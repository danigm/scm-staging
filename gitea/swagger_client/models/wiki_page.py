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
from pydantic import BaseModel, Field, StrictInt, StrictStr
from swagger_client.models.wiki_commit import WikiCommit


class WikiPage(BaseModel):
    """
    WikiPage a wiki page
    """

    commit_count: Optional[StrictInt] = None
    content_base64: Optional[StrictStr] = Field(
        None, description="Page content, base64 encoded"
    )
    footer: Optional[StrictStr] = None
    html_url: Optional[StrictStr] = None
    last_commit: Optional[WikiCommit] = None
    sidebar: Optional[StrictStr] = None
    sub_url: Optional[StrictStr] = None
    title: Optional[StrictStr] = None
    __properties = [
        "commit_count",
        "content_base64",
        "footer",
        "html_url",
        "last_commit",
        "sidebar",
        "sub_url",
        "title",
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
    def from_json(cls, json_str: str) -> WikiPage:
        """Create an instance of WikiPage from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of last_commit
        if self.last_commit:
            _dict["last_commit"] = self.last_commit.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WikiPage:
        """Create an instance of WikiPage from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return WikiPage.parse_obj(obj)

        _obj = WikiPage.parse_obj(
            {
                "commit_count": obj.get("commit_count"),
                "content_base64": obj.get("content_base64"),
                "footer": obj.get("footer"),
                "html_url": obj.get("html_url"),
                "last_commit": WikiCommit.from_dict(obj.get("last_commit"))
                if obj.get("last_commit") is not None
                else None,
                "sidebar": obj.get("sidebar"),
                "sub_url": obj.get("sub_url"),
                "title": obj.get("title"),
            }
        )
        return _obj
