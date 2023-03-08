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
from swagger_client.models.create_milestone_option import (
    CreateMilestoneOption,
)  # noqa: E501
from swagger_client.rest import ApiException


class TestCreateMilestoneOption(unittest.TestCase):
    """CreateMilestoneOption unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CreateMilestoneOption
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `CreateMilestoneOption`
        """
        model = swagger_client.models.create_milestone_option.CreateMilestoneOption()  # noqa: E501
        if include_optional :
            return CreateMilestoneOption(
                description = '', 
                due_on = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                state = 'open', 
                title = ''
            )
        else :
            return CreateMilestoneOption(
        )
        """

    def testCreateMilestoneOption(self):
        """Test CreateMilestoneOption"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
