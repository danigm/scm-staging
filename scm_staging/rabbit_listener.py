"""This module holds the functions listening to the rabbitmq bus of OBS for
package build results and updating the commit status.

"""

import asyncio
import json
from typing import TypedDict
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.spec import Basic
import pika.exceptions
from py_gitea_opensuse_org import ApiClient

from py_gitea_opensuse_org.api.repository_api import RepositoryApi
from py_gitea_opensuse_org.models.pull_request import PullRequest

from scm_staging.ci_status import set_commit_status_from_obs
from scm_staging.webhook import AppConfig


_PREFIX = "opensuse.obs"


class PackageBuildSuccessPayload(TypedDict):
    project: str
    package: str
    repository: str
    arch: str
    release: str
    readytime: str
    srcmd5: str
    rev: str
    reason: str
    bcnt: str
    verifymd5: str
    starttime: str
    endtime: str
    workerid: str
    versrel: str
    buildtype: str


class PackageBuildFailurePayload(PackageBuildSuccessPayload):
    previouslyfailed: str


class PackageBuildUnchangedPayload(PackageBuildSuccessPayload):
    pass


async def pr_from_pkg_name(
    payload: PackageBuildSuccessPayload
    | PackageBuildFailurePayload
    | PackageBuildUnchangedPayload,
    osc_username: str,
    api_client: ApiClient,
) -> PullRequest | None:
    if not f"home:{osc_username}:SCM_STAGING:Factory" in payload["project"]:
        return None

    repo_api = RepositoryApi(api_client)

    repo_name, pr_num = payload["project"].split(":")[-2:]
    if repo_name != payload["package"]:
        raise ValueError(
            f"Mismatch in the package name, got {repo_name} from the project and {payload['package']} from the package itself."
        )
    return await repo_api.repo_get_pull_request(
        "rpm",
        repo_name,
        int(pr_num),
    )


import pika


def main() -> None:
    loop = asyncio.get_event_loop()
    app_config = AppConfig.from_env()

    def callback(
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: pika.BasicProperties,
        body: bytes,
    ) -> None:
        if (method.routing_key or "") not in (
            f"{_PREFIX}.package.build_success",
            f"{_PREFIX}.package.build_fail",
            f"{_PREFIX}.package.build_unchanged",
        ):
            return

        try:
            payload: PackageBuildSuccessPayload | PackageBuildFailurePayload = (
                json.loads(body.decode())
            )
            pr = loop.run_until_complete(
                pr_from_pkg_name(
                    payload, app_config.osc.username, app_config._api_client
                )
            )
            if pr:
                loop.run_until_complete(
                    set_commit_status_from_obs(
                        app_config.osc,
                        app_config._api_client,
                        commit_sha=(head := pr.head).sha,
                        repo_name=(repo := head.repo).name,
                        repo_owner=repo.owner.login,
                        pkg_name=payload["package"],
                        project_name=payload["project"],
                    )
                )
        except Exception:
            pass

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.URLParameters("amqps://opensuse:opensuse@rabbit.opensuse.org")
            )
            channel = connection.channel()

            channel.exchange_declare(
                exchange="pubsub",
                exchange_type=ExchangeType.topic,
                passive=True,
                durable=True,
            )

            result = channel.queue_declare("", exclusive=True)
            queue_name = result.method.queue
            assert queue_name

            channel.queue_bind(exchange="pubsub", queue=queue_name, routing_key="#")

            channel.basic_consume(queue_name, callback, auto_ack=True)

            channel.start_consuming()

        except pika.exceptions.ConnectionClosedByBroker:
            # Uncomment this to make the example not attempt recovery
            # from server-initiated connection closure, including
            # when the node is stopped cleanly
            #
            # break
            continue
        # Do not recover on channel errors
        except pika.exceptions.AMQPChannelError as err:
            print("Caught a channel error: {}, stopping...".format(err))
            break
        # Recover on all other connection errors
        except pika.exceptions.AMQPConnectionError:
            print("Connection was closed, retrying...")
            continue
