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


from typing import List, Optional
from pydantic import BaseModel, StrictBool, conlist
from swagger_client.models.team import Team


class TeamSearch200Response(BaseModel):
    """
    TeamSearch200Response
    """

    data: Optional[conlist(Team)] = None
    ok: Optional[StrictBool] = None
    __properties = ["data", "ok"]

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
    def from_json(cls, json_str: str) -> TeamSearch200Response:
        """Create an instance of TeamSearch200Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in data (list)
        _items = []
        if self.data:
            for _item in self.data:
                if _item:
                    _items.append(_item.to_dict())
            _dict["data"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TeamSearch200Response:
        """Create an instance of TeamSearch200Response from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return TeamSearch200Response.parse_obj(obj)

        _obj = TeamSearch200Response.parse_obj(
            {
                "data": [Team.from_dict(_item) for _item in obj.get("data")]
                if obj.get("data") is not None
                else None,
                "ok": obj.get("ok"),
            }
        )
        return _obj
