"""This module contains the tornado web-application with the webhook listening
for gitea events.

"""

import asyncio
import json
from dataclasses import dataclass, field
from enum import StrEnum, unique
import os
from aiohttp import ClientResponseError

from pydantic import BaseModel, ValidationError
import tornado
from tornado.options import define, options

from py_gitea_opensuse_org import (
    Configuration,
    ApiClient,
    IssueApi,
    CreateIssueCommentOption,
    RepositoryApi,
    PullReview,
)
from py_obs.osc import Osc
from py_obs import request
from py_obs.request import RequestActionType
from py_obs.request import RequestStatus
from py_obs.xml_factory import StrElementField
from py_obs import project
from tornado.web import Application

from scm_staging.ci_status import set_commit_status_from_obs
from scm_staging.config import BranchConfig, SubmissionStyle, load_config
from scm_staging.logger import LOGGER
from scm_staging.db import (
    PullRequestToSubmitRequest,
    create_db,
    insert_submit_request,
    remove_submit_request,
)


class User(BaseModel):
    id: int
    login: str
    full_name: str
    email: str


class Label(BaseModel):
    id: int
    name: str
    color: str
    description: str
    url: str


class Milestone(BaseModel):
    id: int
    title: str
    description: str
    state: str
    open_issues: int
    closed_issues: int


class Repository(BaseModel):
    id: int
    owner: User
    name: str
    full_name: str
    description: str
    html_url: str
    ssh_url: str
    clone_url: str


class Ref(BaseModel):
    label: str
    ref: str
    sha: str
    repo_id: int
    repo: Repository


@unique
class PullRequestReviewType(StrEnum):
    APPROVED = "pull_request_review_approved"
    REJECTED = "pull_request_review_rejected"
    COMMENT = "pull_request_comment"


class Review(BaseModel):
    type: PullRequestReviewType | str
    content: str


class PullRequest(BaseModel):
    id: int
    url: str
    number: int
    user: User
    title: str
    body: str
    labels: list[Label]
    milestone: Milestone | None
    assignee: User | None
    assignees: list[User] | None
    state: str
    is_locked: bool
    base: Ref
    head: Ref
    merge_base: str
    # FIXME: is a date
    created_at: str
    # FIXME: is a date
    updated_at: str


class PullRequestPayload(BaseModel):
    action: str
    number: int
    pull_request: PullRequest
    sender: User
    repository: Repository
    review: Review | None


DEFAULT_DB_NAME = "submit_requests.db"


@dataclass(frozen=True)
class AppConfig:
    gitea_user: str
    branch_config: list[BranchConfig]
    osc: Osc
    db_file_name: str = DEFAULT_DB_NAME

    _conf: Configuration = field(default_factory=Configuration)
    _api_client: ApiClient = field(default_factory=lambda: ApiClient(Configuration()))

    @staticmethod
    def from_env() -> "AppConfig":
        api_key = os.getenv("GITEA_API_KEY")
        if not api_key:
            raise ValueError("GITEA_API_KEY environment variable must be set")

        conf = Configuration(
            api_key={"AuthorizationHeaderToken": api_key},
            api_key_prefix={"AuthorizationHeaderToken": "token"},
            host="https://gitea.opensuse.org/api/v1",
        )

        return AppConfig(
            osc=(osc := Osc.from_env()),
            gitea_user=os.getenv("BOT_USER", osc.username),
            branch_config=load_config(os.getenv("BRANCH_CONFIG", "config.json")),
            db_file_name=os.getenv("DB_FILE_NAME", DEFAULT_DB_NAME),
            _conf=conf,
            _api_client=ApiClient(conf),
        )


def package_from_pull_request(payload: PullRequestPayload) -> project.Package:
    return project.Package(
        name=payload.repository.name,
        title=StrElementField(f"The {payload.repository.name} package"),
        url=StrElementField(payload.pull_request.url),
        scmsync=StrElementField(
            f"{payload.pull_request.head.repo.clone_url}#{payload.pull_request.head.sha}"
        ),
    )


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, app_config: AppConfig) -> None:
        self.app_config = app_config

    def project_from_pull_request(self, payload: PullRequestPayload) -> project.Project:
        pr = payload.pull_request
        return project.Project(
            name=f"home:{self.app_config.osc.username}:SCM_STAGING:{payload.repository.name}:{pr.number}",
            title=StrElementField(f"Project for Pull Request {pr.number}"),
            description=StrElementField(f"Project for Pull Request {pr.url}"),
            person=[
                project.Person(
                    userid=self.app_config.osc.username,
                    role=project.PersonRole.MAINTAINER,
                )
            ],
            repository=[
                project.Repository(
                    name="openSUSE_Factory",
                    arch=["x86_64"],
                    path=[
                        project.PathEntry(
                            project="openSUSE:Factory", repository="snapshot"
                        )
                    ],
                )
            ],
        )

    async def check_if_pr_approved(
        self,
        api_client: ApiClient,
        owner: str,
        repo_name: str,
        pr_number: int,
        pkg_name: str,
    ) -> bool:
        """Checks if the pull request $owner/$repo_name/$pr_number has been approved
        by at least one maintainer of the package `pkg_name` and no changes have
        been requested.

        """
        repo_api = RepositoryApi(api_client)
        reviews: list[PullReview] = await repo_api.repo_list_pull_reviews(
            owner, repo_name, pr_number
        )

        maintainers = await project.search_for_maintainers(
            self.app_config.osc,
            pkg_name=pkg_name,
            groups_to_ignore=["factory-maintainers"],
        )
        usernames: list[str] = []
        if maintainers.package:
            usernames.extend(pers.name for pers in maintainers.package)
        if maintainers.project:
            usernames.extend(pers.name for pers in maintainers.project)

        usernames = list(set(usernames))

        valid_reviews = []
        for review in reviews:
            if not review.stale and review.user.login in usernames:
                valid_reviews.append(review)

        if any(review.state == "REQUEST_CHANGES" for review in valid_reviews):
            return False

        if any(review.state == "APPROVED" for review in valid_reviews):
            return True

        return False

    async def find_devel_project(
        self, project_name: str, package_name: str
    ) -> str | None:
        """Retrieve the develproject of the package with the supplied
        ``package_name`` from the project ``project_name``.

        Returns:
            - the develproject name or None if there is none or some error
              occurred

        """
        try:
            pkg = await project.fetch_meta(
                self.app_config.osc, prj=project_name, pkg=package_name
            )
            if pkg.devel:
                return pkg.devel.project
        except Exception as exc:
            LOGGER.error(
                "Failed to retrieve the devel project of %s, got %s", package_name, exc
            )
        return None

    async def post(self) -> None:
        if not self.request.body:
            return

        try:
            payload = PullRequestPayload(**json.loads(self.request.body))
        except ValidationError:
            return

        LOGGER.debug(payload)

        matching_branch_conf: BranchConfig | None = None

        base = payload.pull_request.base
        for conf in self.app_config.branch_config:
            if (
                base.ref == conf.target_branch_name
                or base.label == conf.target_branch_name
            ) and payload.repository.owner.login == conf.organization:
                LOGGER.debug(
                    "Matched config %s for PR: %s", conf, payload.pull_request.url
                )
                matching_branch_conf = conf
                break

        if matching_branch_conf is None:
            LOGGER.debug(
                "wrong branch name %s or wrong organization %s",
                base.ref,
                payload.repository.owner.login,
            )
            return

        pkg = package_from_pull_request(payload)
        prj = self.project_from_pull_request(payload)

        osc = self.app_config.osc

        if payload.action in ("closed", "merged"):
            tasks = []

            reqs_to_close = await request.search_for_requests(
                osc,
                user=osc.username,
                package=pkg,
                project=prj,
                types=[RequestActionType.SUBMIT],
                states=[
                    RequestStatus.NEW,
                    RequestStatus.DECLINED,
                    RequestStatus.REVIEW,
                ],
            )

            for req in reqs_to_close:
                if req.id and req.creator == osc.username:
                    tasks.append(
                        request.change_state(
                            osc,
                            request=req,
                            new_state=RequestStatus.REVOKED,
                            comment=f"pull request #{payload.pull_request.number} has been closed",
                        )
                    )
                    remove_submit_request(self.app_config.db_file_name, req.id)

            await asyncio.gather(*tasks)
            try:
                await project.delete(osc, prj=prj, force=True)
            except ClientResponseError as cre_exc:
                if cre_exc.status == 404:
                    LOGGER.debug("Not deleting project %s, it doesn't exist", prj.name)
                else:
                    raise
            return

        owner = payload.repository.owner.login
        repo_name = payload.repository.name
        pr_num = payload.pull_request.number

        await set_commit_status_from_obs(
            self.app_config.osc,
            self.app_config._api_client,
            # use "upstream" here, otherwise the commit status will not show up in
            # the PR and will not gate it
            repo_owner=base.repo.owner.login,
            repo_name=base.repo.name,
            commit_sha=payload.pull_request.head.sha,
            pkg_name=pkg.name,
            project_name=prj.name,
        )

        # don't create SRs for not approved PRs
        if matching_branch_conf.require_approval:
            if not await self.check_if_pr_approved(
                self.app_config._api_client,
                owner=owner,
                repo_name=repo_name,
                pr_number=pr_num,
                pkg_name=pkg.name,
            ):
                LOGGER.debug("PR has not been approved, approval required")
                return
            else:
                LOGGER.debug("PR is approved, proceeding")

        await project.send_meta(osc, prj=prj)
        await project.send_meta(osc, prj=prj, pkg=pkg)

        if (
            sr_style := matching_branch_conf.submission_style
        ) == SubmissionStyle.DIRECT:
            dest_prj = matching_branch_conf.destination_project

        elif sr_style == SubmissionStyle.FACTORY_DEVEL:
            dest_prj = await self.find_devel_project(
                matching_branch_conf.destination_project, pkg.name
            )
            if not dest_prj:
                raise ValueError(
                    f"Could not find the develproject for {pkg.name} in {matching_branch_conf.destination_project}"
                )
        else:
            assert False, f"Invalid submission style {sr_style}"

        new_req = await request.submit_package(
            osc,
            source_prj=prj.name,
            pkg_name=pkg.name,
            supersede_old_request=True,
            dest_prj=dest_prj,
            description=f"🤖: Submission of {pkg.name} via {payload.pull_request.url} by {payload.sender.login}",
        )

        create_db(self.app_config.db_file_name)

        insert_submit_request(
            self.app_config.db_file_name,
            PullRequestToSubmitRequest(
                submit_request_id=new_req.id,
                obs_package_name=pkg.name,
                obs_project_name=prj.name,
                gitea_repo_owner=base.repo.owner.login,
                gitea_repo_name=base.repo.name,
                pull_request_number=payload.pull_request.number,
                merge_pr=matching_branch_conf.merge_pr,
            ),
        )

        # comment on the PR with a link to the SR
        issue_api = IssueApi(self.app_config._api_client)
        await issue_api.issue_create_comment(
            payload.repository.owner.login,
            payload.repository.name,
            payload.pull_request.number,
            body=CreateIssueCommentOption(
                body=f"Created submit request [sr#{new_req.id}](https://build.opensuse.org/request/show/{new_req.id})"
            ),
        )


def make_app(app_config: AppConfig) -> Application:
    return Application([(r"/hook", MainHandler, {"app_config": app_config})])


"""
Tornado options and define from command line e.g. --port 8000
"""
define("port", default=8000, help="Tornado web service port listen on")
define("log", default=None, help="Filename for scm_staging log, default to console")
define(
    "access_log",
    default=None,
    help="Filename for Tornado access log, default to console",
)
define(
    "app_log",
    default=None,
    help="Filename for Tornado application log, default to console",
)
define(
    "general_log",
    default=None,
    help="Filename for Tornado general log, default to console",
)


def main():
    options.parse_command_line()
    LOGGER.configure_log_files(
        options.log, options.access_log, options.app_log, options.general_log
    )
    app_config = AppConfig.from_env()
    app = make_app(app_config)
    app.listen(options.port)
    shutdown_event = asyncio.Event()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(shutdown_event.wait())
    finally:
        loop.run_until_complete(app_config.osc.teardown())
