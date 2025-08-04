##############################################################################
# Copyright 2019 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################

"""
Exception definitions.
"""

from http import HTTPStatus

from pyds8k import messages
from pyds8k.utils import get_response_parser_class, get_subclasses


class BaseRestError(Exception):
    pass


class InvalidArgumentError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return messages.INVALID_ARGUMENT.format(self.reason)


class InvalidMethodForCreate(Exception):
    def __init__(self, method):
        self.method = method

    def __str__(self):
        return messages.INVALID_ARGUMINVALID_METHOD_FOR_CREATE.format(self.method)


class OperationNotAllowed(Exception):
    """
    The operation performed on the resource is not allowed.
    """

    def __init__(self, operation_name, resource_name=''):
        self.operation_name = operation_name
        self.resource_name = resource_name

    def __str__(self):
        return messages.OPERATION_NOT_ALLOWED.format(
            self.operation_name, self.resource_name
        )


class URLNotSpecifiedError(Exception):
    """
    The URL is not specified.
    """

    def __str__(self):
        return messages.URL_NOT_SPECIFIED


class URLMissingError(Exception):
    """
    The URL is missing.
    """

    def __str__(self):
        return messages.URL_MISSING


class IDMissingError(Exception):
    """
    The id field is missing or None.
    """

    def __str__(self):
        return messages.ID_MISSING


class ResponseBodyMissingError(Exception):
    """
    The response body is missing.
    """

    def __str__(self):
        return messages.RESPONSE_BODY_MISSING


class URLParseError(Exception):
    """
    Can not get the URL
    """

    def __str__(self):
        return messages.CAN_NOT_GET_URL


class RepresentationNotFoundError(Exception):
    """
    Can not find the representation
    """

    def __str__(self):
        return messages.REPRESENTATION_NOT_FOUND


class RepresentationParseError(Exception):
    """
    Can not get the representation
    """

    def __str__(self):
        return messages.CAN_NOT_GET_REPRESENTATION


class FieldReadOnly(Exception):
    """
    Field is read only.
    """

    def __init__(self, field_name):
        self.field_name = field_name

    def __str__(self):
        return messages.FIELD_READONLY.format(self.field_name)


class ConnectionError(Exception):  # noqa: A001
    """
    Could not open a connection to the API service.
    """


class Timeout(Exception):
    """
    The request timed out.
    """

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return messages.REQUEST_TIMED_OUT.format(self.url)


class ClientException(Exception):
    """
    The base exception class for all HTTP client or server errors.
    """

    def __init__(self, code, message=None, detail='', origin_data=None):
        self.code = code
        self.message = message
        self.detail = detail
        self.error_data = origin_data
        if self.message and self.detail:
            self.details = f'[{self.message}] {self.detail}'
        elif self.message or self.detail:
            self.details = self.message or self.detail
        else:
            self.details = ''

    def __str__(self):
        return f"HTTP {self.code} {self.reason_phrase}. {self.details}"


class ClientError(ClientException):
    """
    HTTP 4xx - Client Error
    """

    status_code = '4xx'
    reason_phrase = "Client Error"


class ServerError(ClientException):
    """
    HTTP 5xx - Server Error
    """

    status_code = '5xx'
    reason_phrase = "Server Error"


class BadRequest(ClientError):
    """
    HTTP 400 - Bad request: you sent some malformed data.
    """

    status_code = str(HTTPStatus.BAD_REQUEST.value)
    reason_phrase = HTTPStatus.BAD_REQUEST.phrase


class Unauthorized(ClientError):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """

    status_code = str(HTTPStatus.UNAUTHORIZED.value)
    reason_phrase = HTTPStatus.UNAUTHORIZED.phrase


class Forbidden(ClientError):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """

    status_code = str(HTTPStatus.FORBIDDEN.value)
    reason_phrase = HTTPStatus.FORBIDDEN.phrase


class NotFound(ClientError):
    """
    HTTP 404 - Not found
    """

    status_code = str(HTTPStatus.NOT_FOUND.value)
    reason_phrase = HTTPStatus.NOT_FOUND.phrase


class MethodNotAllowed(ClientError):
    """
    HTTP 405 - Method Not Allowed
    """

    status_code = str(HTTPStatus.METHOD_NOT_ALLOWED.value)
    reason_phrase = HTTPStatus.METHOD_NOT_ALLOWED.phrase


class Conflict(ClientError):
    """
    HTTP 409 - Conflict
    """

    status_code = str(HTTPStatus.CONFLICT.value)
    reason_phrase = HTTPStatus.CONFLICT.phrase


class UnsupportedMediaType(ClientError):
    """
    HTTP 415 - Unsupported Media Type
    """

    status_code = str(HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value)
    reason_phrase = HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase


class InternalServerError(ServerError):
    """
    HTTP 500 - Internal Server Error: The server encountered an unexpected
    condition which prevented it from fulfilling the request.
    """

    status_code = str(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    reason_phrase = HTTPStatus.INTERNAL_SERVER_ERROR.phrase


class ServiceUnavailable(ServerError):
    """
    HTTP 503 - Service Unavailable
    """

    status_code = str(HTTPStatus.SERVICE_UNAVAILABLE.value)
    reason_phrase = HTTPStatus.SERVICE_UNAVAILABLE.phrase


class GatewayTimeout(ServerError):
    """
    HTTP 504 - Gateway Timeout
    """

    status_code = str(HTTPStatus.GATEWAY_TIMEOUT.value)
    reason_phrase = HTTPStatus.GATEWAY_TIMEOUT.phrase


_error_dict = {c.status_code: c for c in get_subclasses(ClientException)}


def raise_error(response, body, service_type=''):
    """
    Return an instance of an ClientException or subclass
    based on an requests response.
    """
    ResponseParser = get_response_parser_class(service_type)  # noqa: N806
    cls = _error_dict.get(str(response.status_code), ClientException)
    if body:
        res_p = ResponseParser(body)
        message = res_p.get_error_code()
        details = res_p.get_error_msg()
        data = res_p.get_status_body()
        return cls(
            code=response.status_code, message=message, detail=details, origin_data=data
        )
    return cls(code=response.status_code, message=response.reason, origin_data=body)
