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

# ==============================================================================
# restclient.exceptions
# ==============================================================================
OPERATION_NOT_ALLOWED = 'OperationNotAllowed: the {} operation you performed \
on resource {} is not allowed.'
URL_NOT_SPECIFIED = 'The URL is missing, you must specify a valid URL here.'
URL_MISSING = 'Can not get URL, the URL here is missing.'
ID_MISSING = 'The id field of current resource is missing or not specified.'
FIELD_READONLY = 'The field {} is read only.'
CAN_NOT_GET_URL = 'Can not get URL.'
RESPONSE_BODY_MISSING = 'The response has no content.'
CAN_NOT_GET_REPRESENTATION = 'Can not get the requested resource from \
returned data.'
REQUEST_TIMED_OUT = 'Connection to {} timed out.'
INVALID_ARGUMENT = 'InvalidArgument: {}'

# ==============================================================================
# restclient.utils
# ==============================================================================
GET_CONFIG_SETTINGS_IOERROR = 'IOError: error opening config file:{0}, e={1}'
GET_CONFIG_SETTINGS_ERROR = 'Exception in get_config_settings. e={0}'


# ==============================================================================
# restclient.httpclient
# ==============================================================================
CONNECTION_ERROR = 'Unable to establish connection: {}'
REAUTH_SERVER = 'Unauthorized, reauthenticating...'
REDIRECTING = 'The url "{}" you requested is moved permanently, redirecting \
to the new url "{}"...'


# ==============================================================================
# restclient.base
# ==============================================================================
CAN_NOT_GET_STATUS_BODY = 'Can not get the status body in {} {} response, \
will return the original response body.'
DEFAULT_SUCCESS_BODY_DICT = {
    'status': 'ok',
    'message': 'Operation done successfully.'
}
DEFAULT_FAIL_BODY_JSON = '{{"status": "failed", "message": \
"Can not {action} {res_class} {res_id}"}}'
SET_RELATED_RESOURCE_FAILED = 'Can not set {} during loading {}'


# ==============================================================================
# restclient.dataParser.ds8k
# ==============================================================================
NEED_A_DICT_OR_DICT_LIST = 'data must be a dict or a dict list. Raw data is {}'
REPRESENTATION_NOT_FOUND = 'No representation is specified'
STATUS_BODY_NOT_FOUND = 'failed to get status body'


# ==============================================================================
# restclient.resources.ds8k
# ==============================================================================
INVALID_TYPE = 'Invalid type you specified, expected one of: {}.'
INVALID_LSS_TYPE = 'Invalid lss type. Expected one of: {}.'
INVALID_NAME = \
    r'Invalid volume name. The right format is: {nameprefix}_{volume_id}'
INVALID_POOL_NAME = \
    r'Invalid pool name. The right format is: {pool_name}_{pool_id}'
ITEM_IN_LIST = '{} [{}] are already existed.'
ITEM_NOT_IN_LIST = '{0} [{1}] are not in the current {0}.'
