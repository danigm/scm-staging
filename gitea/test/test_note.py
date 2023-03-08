# coding: utf-8

"""
    Gitea API.

    This documentation describes the Gitea API.  # noqa: E501

    The version of the OpenAPI document: 1.19
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import unittest
import datetime

import swagger_client
from swagger_client.models.note import Note  # noqa: E501
from swagger_client.rest import ApiException


class TestNote(unittest.TestCase):
    """Note unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Note
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `Note`
        """
        model = swagger_client.models.note.Note()  # noqa: E501
        if include_optional :
            return Note(
                commit = swagger_client.models.commit_contains_information_generated_from_a_git_commit/.Commit contains information generated from a Git commit.(
                    author = swagger_client.models.user.User(
                        active = True, 
                        avatar_url = '', 
                        created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        description = '', 
                        email = '', 
                        followers_count = 56, 
                        following_count = 56, 
                        full_name = '', 
                        id = 56, 
                        is_admin = True, 
                        language = '', 
                        last_login = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        location = '', 
                        login = '', 
                        login_name = 'empty', 
                        prohibit_login = True, 
                        restricted = True, 
                        starred_repos_count = 56, 
                        visibility = '', 
                        website = '', ), 
                    commit = swagger_client.models.repo_commit_contains_information_of_a_commit_in_the_context_of_a_repository/.RepoCommit contains information of a commit in the context of a repository.(
                        committer = swagger_client.models.commit_user_contains_information_of_a_user_in_the_context_of_a_commit/.CommitUser contains information of a user in the context of a commit.(
                            date = '', 
                            email = '', 
                            name = '', ), 
                        message = '', 
                        tree = swagger_client.models.commit_meta_contains_meta_information_of_a_commit_in_terms_of_api/.CommitMeta contains meta information of a commit in terms of API.(
                            created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            sha = '', 
                            url = '', ), 
                        url = '', 
                        verification = swagger_client.models.payload_commit_verification.PayloadCommitVerification(
                            payload = '', 
                            reason = '', 
                            signature = '', 
                            signer = swagger_client.models.payload_user.PayloadUser(
                                email = '', 
                                name = '', 
                                username = '', ), 
                            verified = True, ), ), 
                    committer = swagger_client.models.user.User(
                        active = True, 
                        avatar_url = '', 
                        created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        description = '', 
                        email = '', 
                        followers_count = 56, 
                        following_count = 56, 
                        full_name = '', 
                        id = 56, 
                        is_admin = True, 
                        language = '', 
                        last_login = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        location = '', 
                        login = '', 
                        login_name = 'empty', 
                        prohibit_login = True, 
                        restricted = True, 
                        starred_repos_count = 56, 
                        visibility = '', 
                        website = '', ), 
                    created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                    files = [
                        swagger_client.models.commit_affected_files.CommitAffectedFiles(
                            filename = '', )
                        ], 
                    html_url = '', 
                    parents = [
                        swagger_client.models.commit_meta_contains_meta_information_of_a_commit_in_terms_of_api/.CommitMeta contains meta information of a commit in terms of API.(
                            created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                            sha = '', 
                            url = '', )
                        ], 
                    sha = '', 
                    stats = swagger_client.models.commit_stats.CommitStats(
                        additions = 56, 
                        deletions = 56, 
                        total = 56, ), 
                    url = '', ), 
                message = ''
            )
        else :
            return Note(
        )
        """

    def testNote(self):
        """Test Note"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
