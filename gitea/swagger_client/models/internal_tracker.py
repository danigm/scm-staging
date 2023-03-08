# coding: utf-8

"""
    Gitea API.

    This documentation describes the Gitea API.  # noqa: E501

    The version of the OpenAPI document: 1.19
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
from inspect import getfullargspec
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictBool


class InternalTracker(BaseModel):
    """
    InternalTracker represents settings for internal tracker
    """

    allow_only_contributors_to_track_time: Optional[StrictBool] = Field(
        None, description="Let only contributors track time (Built-in issue tracker)"
    )
    enable_issue_dependencies: Optional[StrictBool] = Field(
        None,
        description="Enable dependencies for issues and pull requests (Built-in issue tracker)",
    )
    enable_time_tracker: Optional[StrictBool] = Field(
        None, description="Enable time tracking (Built-in issue tracker)"
    )
    __properties = [
        "allow_only_contributors_to_track_time",
        "enable_issue_dependencies",
        "enable_time_tracker",
    ]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> InternalTracker:
        """Create an instance of InternalTracker from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InternalTracker:
        """Create an instance of InternalTracker from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return InternalTracker.parse_obj(obj)

        _obj = InternalTracker.parse_obj(
            {
                "allow_only_contributors_to_track_time": obj.get(
                    "allow_only_contributors_to_track_time"
                ),
                "enable_issue_dependencies": obj.get("enable_issue_dependencies"),
                "enable_time_tracker": obj.get("enable_time_tracker"),
            }
        )
        return _obj
