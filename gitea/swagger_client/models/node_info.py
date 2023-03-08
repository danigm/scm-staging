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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr, conlist
from swagger_client.models.node_info_services import NodeInfoServices
from swagger_client.models.node_info_software import NodeInfoSoftware
from swagger_client.models.node_info_usage import NodeInfoUsage


class NodeInfo(BaseModel):
    """
    NodeInfo contains standardized way of exposing metadata about a server running one of the distributed social networks
    """

    metadata: Optional[Dict[str, Any]] = None
    open_registrations: Optional[StrictBool] = Field(None, alias="openRegistrations")
    protocols: Optional[conlist(StrictStr)] = None
    services: Optional[NodeInfoServices] = None
    software: Optional[NodeInfoSoftware] = None
    usage: Optional[NodeInfoUsage] = None
    version: Optional[StrictStr] = None
    __properties = [
        "metadata",
        "openRegistrations",
        "protocols",
        "services",
        "software",
        "usage",
        "version",
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
    def from_json(cls, json_str: str) -> NodeInfo:
        """Create an instance of NodeInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True, exclude={}, exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of services
        if self.services:
            _dict["services"] = self.services.to_dict()
        # override the default output from pydantic by calling `to_dict()` of software
        if self.software:
            _dict["software"] = self.software.to_dict()
        # override the default output from pydantic by calling `to_dict()` of usage
        if self.usage:
            _dict["usage"] = self.usage.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> NodeInfo:
        """Create an instance of NodeInfo from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return NodeInfo.parse_obj(obj)

        _obj = NodeInfo.parse_obj(
            {
                "metadata": obj.get("metadata"),
                "open_registrations": obj.get("openRegistrations"),
                "protocols": obj.get("protocols"),
                "services": NodeInfoServices.from_dict(obj.get("services"))
                if obj.get("services") is not None
                else None,
                "software": NodeInfoSoftware.from_dict(obj.get("software"))
                if obj.get("software") is not None
                else None,
                "usage": NodeInfoUsage.from_dict(obj.get("usage"))
                if obj.get("usage") is not None
                else None,
                "version": obj.get("version"),
            }
        )
        return _obj
