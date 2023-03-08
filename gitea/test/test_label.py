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
from swagger_client.models.label import Label  # noqa: E501
from swagger_client.rest import ApiException


class TestLabel(unittest.TestCase):
    """Label unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Label
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `Label`
        """
        model = swagger_client.models.label.Label()  # noqa: E501
        if include_optional :
            return Label(
                color = '00aabb', 
                description = '', 
                exclusive = False, 
                id = 56, 
                name = '', 
                url = ''
            )
        else :
            return Label(
        )
        """

    def testLabel(self):
        """Test Label"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
