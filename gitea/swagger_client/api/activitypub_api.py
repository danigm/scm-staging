# coding: utf-8

"""
    Gitea API.

    This documentation describes the Gitea API.  # noqa: E501

    The version of the OpenAPI document: 1.19
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


import re  # noqa: F401

from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated
from typing import overload, Optional, Union, Awaitable

from pydantic import Field, StrictStr

from swagger_client.models.activity_pub import ActivityPub

from swagger_client.api_client import ApiClient
from swagger_client.exceptions import ApiTypeError, ApiValueError  # noqa: F401


class ActivitypubApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @overload
    async def activitypub_person(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        **kwargs
    ) -> ActivityPub:  # noqa: E501
        ...

    @overload
    def activitypub_person(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        async_req: Optional[bool] = True,
        **kwargs
    ) -> ActivityPub:  # noqa: E501
        ...

    @validate_arguments
    def activitypub_person(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        async_req: Optional[bool] = None,
        **kwargs
    ) -> Union[ActivityPub, Awaitable[ActivityPub]]:  # noqa: E501
        """Returns the Person actor for a user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activitypub_person(username, async_req=True)
        >>> result = thread.get()

        :param username: username of the user (required)
        :type username: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: ActivityPub
        """
        kwargs["_return_http_data_only"] = True
        if async_req is not None:
            kwargs["async_req"] = async_req
        return self.activitypub_person_with_http_info(username, **kwargs)  # noqa: E501

    @validate_arguments
    def activitypub_person_with_http_info(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        **kwargs
    ):  # noqa: E501
        """Returns the Person actor for a user  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activitypub_person_with_http_info(username, async_req=True)
        >>> result = thread.get()

        :param username: username of the user (required)
        :type username: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(ActivityPub, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = ["username"]
        _all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
                "_content_type",
                "_headers",
            ]
        )

        # validate the arguments
        for _key, _val in _params["kwargs"].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method activitypub_person" % _key
                )
            _params[_key] = _val
        del _params["kwargs"]

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params["username"]:
            _path_params["username"] = _params["username"]

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get("_headers", {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # set the HTTP header `Accept`
        _header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # authentication setting
        _auth_settings = [
            "TOTPHeader",
            "AuthorizationHeaderToken",
            "SudoHeader",
            "BasicAuth",
            "AccessToken",
            "SudoParam",
            "Token",
        ]  # noqa: E501

        _response_types_map = {
            "200": "ActivityPub",
        }

        return self.api_client.call_api(
            "/activitypub/user/{username}",
            "GET",
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get("async_req"),
            _return_http_data_only=_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=_params.get("_preload_content", True),
            _request_timeout=_params.get("_request_timeout"),
            collection_formats=_collection_formats,
            _request_auth=_params.get("_request_auth"),
        )

    @overload
    async def activitypub_person_inbox(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        **kwargs
    ) -> None:  # noqa: E501
        ...

    @overload
    def activitypub_person_inbox(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        async_req: Optional[bool] = True,
        **kwargs
    ) -> None:  # noqa: E501
        ...

    @validate_arguments
    def activitypub_person_inbox(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        async_req: Optional[bool] = None,
        **kwargs
    ) -> Union[None, Awaitable[None]]:  # noqa: E501
        """Send to the inbox  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activitypub_person_inbox(username, async_req=True)
        >>> result = thread.get()

        :param username: username of the user (required)
        :type username: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """
        kwargs["_return_http_data_only"] = True
        if async_req is not None:
            kwargs["async_req"] = async_req
        return self.activitypub_person_inbox_with_http_info(
            username, **kwargs
        )  # noqa: E501

    @validate_arguments
    def activitypub_person_inbox_with_http_info(
        self,
        username: Annotated[StrictStr, Field(..., description="username of the user")],
        **kwargs
    ):  # noqa: E501
        """Send to the inbox  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.activitypub_person_inbox_with_http_info(username, async_req=True)
        >>> result = thread.get()

        :param username: username of the user (required)
        :type username: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: None
        """

        _params = locals()

        _all_params = ["username"]
        _all_params.extend(
            [
                "async_req",
                "_return_http_data_only",
                "_preload_content",
                "_request_timeout",
                "_request_auth",
                "_content_type",
                "_headers",
            ]
        )

        # validate the arguments
        for _key, _val in _params["kwargs"].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method activitypub_person_inbox" % _key
                )
            _params[_key] = _val
        del _params["kwargs"]

        _collection_formats = {}

        # process the path parameters
        _path_params = {}
        if _params["username"]:
            _path_params["username"] = _params["username"]

        # process the query parameters
        _query_params = []
        # process the header parameters
        _header_params = dict(_params.get("_headers", {}))
        # process the form parameters
        _form_params = []
        _files = {}
        # process the body parameter
        _body_params = None
        # authentication setting
        _auth_settings = [
            "TOTPHeader",
            "AuthorizationHeaderToken",
            "SudoHeader",
            "BasicAuth",
            "AccessToken",
            "SudoParam",
            "Token",
        ]  # noqa: E501

        _response_types_map = {}

        return self.api_client.call_api(
            "/activitypub/user/{username}/inbox",
            "POST",
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get("async_req"),
            _return_http_data_only=_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=_params.get("_preload_content", True),
            _request_timeout=_params.get("_request_timeout"),
            collection_formats=_collection_formats,
            _request_auth=_params.get("_request_auth"),
        )
