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
from swagger_client.models.push_mirror import PushMirror  # noqa: E501
from swagger_client.rest import ApiException


class TestPushMirror(unittest.TestCase):
    """PushMirror unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PushMirror
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `PushMirror`
        """
        model = swagger_client.models.push_mirror.PushMirror()  # noqa: E501
        if include_optional :
            return PushMirror(
                created = '', 
                interval = '', 
                last_error = '', 
                last_update = '', 
                remote_address = '', 
                remote_name = '', 
                repo_name = '', 
                sync_on_commit = True
            )
        else :
            return PushMirror(
        )
        """

    def testPushMirror(self):
        """Test PushMirror"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
