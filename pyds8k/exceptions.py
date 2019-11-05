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

from pyds8k.utils import get_subclasses, \
    get_response_parser_class
from pyds8k import messages


class BaseRestError(Exception):
    pass


class InvalidArgumentError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return messages.INVALID_ARGUMENT.format(
            self.reason
        )


class OperationNotAllowed(Exception):
    """
    The operation performed on the resource is not allowed.
    """
    def __init__(self, operation_name, resource_name=''):
        self.operation_name = operation_name
        self.resource_name = resource_name

    def __str__(self):
        return messages.OPERATION_NOT_ALLOWED.format(
            self.operation_name,
            self.resource_name
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


class ConnectionError(Exception):
    """
    Could not open a connection to the API service.
    """
    pass


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
            self.details = '[{}] {}'.format(self.message, self.detail)
        elif self.message or self.detail:
            self.details = self.message or self.detail
        else:
            self.details = ''

    def __str__(self):
        return "HTTP {0} {1}. {2}".format(
            self.code,
            self.reason_phrase,
            self.details
        )


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
    status_code = '400'
    reason_phrase = "Bad Request"


class Unauthorized(ClientError):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    status_code = '401'
    reason_phrase = "Unauthorized"


class Forbidden(ClientError):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    status_code = '403'
    reason_phrase = "Forbidden"


class NotFound(ClientError):
    """
    HTTP 404 - Not found
    """
    status_code = '404'
    reason_phrase = "Not Found"


class MethodNotAllowed(ClientError):
    """
    HTTP 405 - Method Not Allowed
    """
    status_code = '405'
    reason_phrase = "Method Not Allowed"


class Conflict(ClientError):
    """
    HTTP 409 - Conflict
    """
    status_code = '409'
    reason_phrase = "Conflict"


class UnsupportedMediaType(ClientError):
    """
    HTTP 415 - Unsupported Media Type
    """
    status_code = '415'
    reason_phrase = "Unsupported Media Type"


class InternalServerError(ServerError):
    """
    HTTP 500 - Internal Server Error: The server encountered an unexpected
    condition which prevented it from fulfilling the request.
    """
    status_code = '500'
    reason_phrase = "Internal Server Error"


class ServiceUnavailable(ServerError):
    """
    HTTP 503 - Service Unavailable
    """
    status_code = '503'
    reason_phrase = "Service Unavailable"


class GatewayTimeout(ServerError):
    """
    HTTP 504 - Gateway Timeout
    """
    status_code = '504'
    reason_phrase = "Gateway Timeout"


_error_dict = dict((c.status_code, c) for c in get_subclasses(ClientException))


def raise_error(response, body, service_type=''):
    """
    Return an instance of an ClientException or subclass
    based on an requests response.
    """
    ResponseParser = get_response_parser_class(service_type)
    cls = _error_dict.get(str(response.status_code), ClientException)
    if body:
        res_p = ResponseParser(body)
        message = res_p.get_error_code()
        details = res_p.get_error_msg()
        data = res_p.get_status_body()
        return cls(code=response.status_code,
                   message=message,
                   detail=details,
                   origin_data=data
                   )
    else:
        return cls(code=response.status_code,
                   message=response.reason,
                   origin_data=body
                   )
