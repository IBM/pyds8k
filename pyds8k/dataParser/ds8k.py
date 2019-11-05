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

from logging import getLogger
from pyds8k import PYDS8K_DEFAULT_LOGGER
from pyds8k.dataParser.base import BaseRequestParser, \
    BaseResponseParser
from pyds8k import messages
from pyds8k.exceptions import URLParseError, \
    RepresentationParseError, \
    IDMissingError

logger = getLogger(PYDS8K_DEFAULT_LOGGER)

success_status = ('ok', 'successful', )


class RequestParser(BaseRequestParser):
    """
    Parse the data user wants to send to server,
    in the right format that server defined.
    """
    request_key = 'request'
    request_key_multi = 'request'
    param_key = 'params'

    def __init__(self, raw_data, resource_key=''):
        if not (isinstance(raw_data, list) or isinstance(raw_data, dict)):
            raise TypeError(messages.NEED_A_DICT_OR_DICT_LIST.format(raw_data))
        self.raw_data = raw_data
        self.request_data = None

    def get_raw_data(self):
        return self.raw_data

    def get_request_data(self):
        data = {}
        if not isinstance(self.raw_data, list):
            data[self.request_key] = {self.param_key: {}}
            data[self.request_key][self.param_key].update(self.raw_data)
        else:
            data[self.request_key_multi] = {self.param_key: []}
            for d in self.raw_data:
                data[self.request_key_multi][self.param_key].append(d)
        self.request_data = data
        return data


class ResponseParser(BaseResponseParser):
    """
    Parse response data, to get resource link, representation, etc.
    """
    response_key = 'data'
    status_key = 'server'
    url_field = 'link'

    def __init__(self, raw_data, resource_key=''):
        self.raw_data = raw_data
        self.resource_key = resource_key
        self.representations = None
        self.representation = None
        self.status_body = None

    def get_raw_data(self):
        return self.raw_data

    def get_link(self, representation=None):
        rep = None
        if representation:
            rep = representation
        elif self.representation:
            rep = self.representation
        else:
            raise Exception(messages.REPRESENTATION_NOT_FOUND)
        return self.__class__.get_link_from_representation(rep)

    def get_representations(self):
        data = self.raw_data.get(self.response_key, self.raw_data)
        parsed = self._parse_data(data)
        self.representations = parsed
        return parsed

    def get_posta_response_data(self):
        MULTIFLAG = "responses"
        data = self.raw_data.get(MULTIFLAG, self.raw_data)
        if not isinstance(data, list):
            data = [data, ]
        res = []
        for s_data in data:
            res_status_body = s_data.get(self.status_key)
            status = self.get_status(res_status_body)
            # return data part if the status is ok.
            if str(status).lower() in success_status:
                res_data = s_data.get(self.response_key)
                res_url = self.get_link_from_representation(s_data)
                if not res_data:
                    res.append(({self.resource_data_key: None}, res_url))
                else:
                    res.append(
                        ({self.resource_data_key: self._parse_data(res_data)[0]},  # noqa
                         res_url
                         )
                    )
            # return status part if something failed.
            else:
                res.append(({self.error_status_key: res_status_body}, None))
        return res

    def get_status_body(self):
        self.status_body = self.raw_data.get(self.status_key, self.raw_data)
        return self.status_body

    def get_error_code(self, status_body=None):
        if not self.status_body:
            self.status_body = self.get_status_body()
        data = status_body or self.status_body
        return data.get('code', '')

    def get_error_msg(self, status_body=None):
        if not self.status_body:
            self.status_body = self.get_status_body()
        data = status_body or self.status_body
        return data.get('message', '')

    def get_status(self, status_body=None):
        if not self.status_body:
            self.status_body = self.get_status_body()
        data = status_body or self.status_body
        return data.get('status', '')

    @classmethod
    def get_link_from_representation(cls, representation):
        url_objects = representation.get(cls.url_field)
        if not url_objects:
            return ""
        url = cls._get_url(url_objects)
        return url

    @classmethod
    def get_resource_id_from_url(self, url, resource_type):
        if url.endswith('/'):
            url = url[:-1]
        url_frag = url.split('/')
        if len(url_frag) > 1 and url_frag[-2] == resource_type:
            return url_frag[-1]
        logger.debug("Failed to get resource id from url {}".format(url))
        raise IDMissingError()

    @classmethod
    def _get_url(cls, urls):
        if isinstance(urls, str):
            return urls
        elif isinstance(urls, dict):
            urls = [urls]
        elif isinstance(urls, list):
            pass
        else:
            raise URLParseError()
        for url in urls:
            if url.get('rel') == 'self':
                return url.get('href', '')
        return ''

    def _parse_data(self, data):
        parsed = None
        if isinstance(data, dict):
            if self.resource_key:
                parsed = data.get(self.resource_key)
                if parsed is None:
                    logger.debug(
                        "Failed to parse resource from data, return raw data: {}".format(data)  # noqa
                    )
                    parsed = data
        else:
            raise RepresentationParseError()
        if not isinstance(parsed, list):
            parsed = [parsed]
        return parsed
