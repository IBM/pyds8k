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
from pyds8k import exceptions
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings
from requests.exceptions import Timeout
from pyds8k.auth.authenticate import get_authenticate
from pyds8k.utils import is_absolute_url
from pyds8k.messages import CONNECTION_ERROR, \
    REAUTH_SERVER, \
    REDIRECTING

try:
    import json
except ImportError:
    import simplejson as json

logger = getLogger(PYDS8K_DEFAULT_LOGGER)

DEFAULT_TIMEOUT_SEC = 25
DEFAULT_SERVICE_VERSION = 'v1'

disable_warnings(InsecureRequestWarning)


class HTTPClient(object):
    """
    An HTTP client interacting with RESTAPI web service.

    Args:
     service_address (str): Hostname/IP address of the web service. Required.
     user (str): Username for connecting to the web service. Required.
     password (str): Password for connecting to the web service. Required.
     hostname (str): It is required when the service has a
                     remote backend (eg: a storage system)
     port (int): Port number of the server.
     service_type (str): It is used to decide which series of resources, which
                         auth functions, and which data parsers will take
                         effect when a HTTPClient instance is instantiated.
                         Required. Currently, only 'ds8k' is supported.
     service_version (str): It is used to decide which version of resources,
                            which auth functions, and which data parsers will
                            take effect when a HTTPClient instance is
                            instantiated. Default is "v1"
                            Currently, only "v1" is supported.
     timeout (float): How long to wait for the server to send data
                    before giving up, as a float. In seconds.
                    Default is 25, and 0 means no limitation.
     secure (bool): Use HTTPS if it is True, Default is True.
     cert (str/tuple): If str, path to ssl client cert file(.pem).
                 If tuple, ('cert', 'key') pair. Defaults to None.
     verify (bool/str): (optional) Either a bool, in which case it controls
                 whether we verify the server's TLS certificate, or a string,
                 in which case it must be a path to a CA bundle to use.
                 Defaults to ``True``.
     default_headers (dict): The extra http headers in every request.

    Returns:
        object: An HTTP client interacting with RESTAPI web service.

    """

    USER_AGENT = 'python-restclient'
    DefaultHeaders = {'User-Agent': USER_AGENT,
                      'Accept': 'application/json',
                      }

    def __init__(self, service_address, user, password,
                 service_type,
                 service_version=DEFAULT_SERVICE_VERSION,
                 port=None,
                 hostname=None,
                 secure=True,
                 timeout=DEFAULT_TIMEOUT_SEC,
                 default_headers=None,
                 cert=None,
                 verify=True
                 ):
        self.user = user
        self.password = password
        self.service_type = service_type
        self.service_version = service_version
        self.service_address = service_address.rstrip('/')
        self.hostname = hostname
        self.port = port
        url_service_point = self.service_address
        list_uri = [self.service_address]
        self.schema = None
        if ":" in self.service_address:
            list_uri = self.service_address.split(':')
            if list_uri[0].strip().lower() in ["http", "https"]:
                # found schema string
                self.schema = list_uri[0].strip().lower()
                list_uri = list_uri[1:]

        # if no schema provide, default secure as True set schema to https
        self.schema = self.schema or secure and "https" or "http"
        prefix_http = f"{self.schema}://"

        list_uri[0] = list_uri[0].lstrip("//")
        if len(list_uri) > 1 and "/" != list_uri[1][0]:
            # found embedded port
            self.port = int(list_uri[1].split('/')[0])
            url_service_point = ":".join(list_uri)
        elif len(list_uri) == 1:
            # no port in service address, add port if defined port is not 80
            if "80" != self.port:
                list_seg_sp = list_uri[0].split('/')
                list_seg_sp[0] = f"{list_seg_sp[0]}:{self.port}"
                url_service_point = "/".join(list_seg_sp)
        list_uri = url_service_point.split('/')
        # if context root is provided, default to /api
        if len(list_uri) == 1:
            list_uri.append('api')
        list_uri.append(self.service_version)
        self.service_address = f"{prefix_http}{'/'.join(list_uri)}"
        self.domain = f"{prefix_http}{list_uri[0]}"
        self.base_url = f"/{'/'.join(list_uri[1:])}"
        self.verify = verify if "https" == self.schema else False
        self.cert = cert
        self.timeout = timeout
        self.defaultHeaders = self.DefaultHeaders.copy()
        self.defaultHeaders = dict()
        if default_headers is not None and isinstance(default_headers, dict):
            self.defaultHeaders.update(default_headers)
        self.defaultQuerystrings = {}
        self.authenticate = get_authenticate(
            service_type=self.service_type,
            service_version=self.service_version
        )
        self.session = requests.session()

    @classmethod
    def log_req(cls, args, kwargs):
        string_parts = ['curl -i']
        for element in args:
            if element in ('GET', 'POST', 'DELETE', 'PUT', 'PATCH'):
                string_parts.append(' -X {}'.format(element))
            else:
                string_parts.append(' {}'.format(element))

        for element in kwargs['headers']:
            header = ' -H "{0}: {1}"'.format(
                element,
                kwargs['headers'][element]
            )
            string_parts.append(header)

        if 'data' in kwargs:
            string_parts.append(' -d "{}"'.format(kwargs['data']))
        logger.debug("\nREQ: {}\n".format("".join(string_parts)))

    @classmethod
    def log_resp(cls, resp):
        logger.debug(
            "\nRESP: [{0}] {1}\nRESP BODY: {2}\n".format(
                resp.status_code,
                resp.headers,
                resp.text
            )
        )

    def request(self, url, method, **kwargs):
        log_required = True
        url = url
        headers = kwargs.get('headers', {}).copy()
        with_http_headers = kwargs.get('with_http_headers', {})

        if self.timeout != 0:
            kwargs.setdefault('timeout', self.timeout)

        attempts = 0
        while True:
            if with_http_headers:
                kwargs['headers'] = with_http_headers
            else:
                kwargs['headers'] = {}
                kwargs['headers'].update(self.defaultHeaders)
                kwargs['headers'].update(headers)
            if 'body' in kwargs:
                kwargs['headers']['Content-Type'] = 'application/json'
                kwargs['data'] = json.dumps(kwargs['body'])
                del kwargs['body']
            kwargs['params'] = kwargs.get('params', {})
            kwargs['params'].update(self.defaultQuerystrings)
            if self.authenticate.get_auth_url() in url:
                attempts += 1
                log_required = False
            absolute_url = url if is_absolute_url(url) \
                else self.service_address + url
            if log_required:
                self.log_req(
                    (absolute_url, method,),
                    kwargs
                 )
            try:
                resp = self.session.request(
                    method,
                    absolute_url,
                    verify=self.verify,
                    cert=self.cert,
                    **kwargs)
                self.log_resp(resp)
                if resp.text:
                    try:
                        body = json.loads(resp.text)
                    except ValueError:
                        body = None
                else:
                    body = None
                # Requests will deal with redirect automatically, code here is
                # not needed. You can set allow_redirects=False to disable it.
                if resp.status_code == 301:
                    old_url = url
                    link = self._get_uri_from_location(resp)
                    url = self._parse_url(link)
                    logger.info(REDIRECTING.format(old_url, url))
                    continue

                if resp.status_code >= 400:
                    raise exceptions.raise_error(resp, body, self.service_type)
                return resp, body

            except exceptions.Unauthorized as e:
                if attempts > 0:
                    raise e
                logger.debug(REAUTH_SERVER)
                attempts += 1
                self.authenticate.authenticate(self)
                continue
            except exceptions.BadRequest as e:
                raise e
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Error When Requesting Url: {absolute_url}")
                raise exceptions.ConnectionError(CONNECTION_ERROR.format(e))
            except Timeout as e:
                logger.debug(e)
                raise exceptions.Timeout(absolute_url)

    def get(self, url, **kwargs):
        # logger.info('getting {}'.format(url))
        return self.request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        return self.request(url, 'POST', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url, 'PUT', **kwargs)

    def patch(self, url, **kwargs):
        return self.request(url, 'PATCH', **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url, 'DELETE', **kwargs)

    def set_defaultQuerystrings(self, key, value):
        self.defaultQuerystrings[key] = value

    def set_defaultHeaders(self, key, value):
        self.defaultHeaders[key] = value

    def set_defaultHttpFields(self):
        pass

    def _get_uri_from_location(self, resp):
        link = resp.headers.get('Location')
        if not link:
            raise exceptions.URLParseError()
        return link

    def _parse_url(self, url):
        schma = '{}:'.format(self.schema)
        if '//' in url:
            schma, url1 = url.split('//')
        else:
            url1 = url
        domain, url2 = url1.split('/', 1)
        if not domain:
            return url
        elif schma + '//' + domain == self.domain:
            return '/' + url2
        else:
            raise exceptions.URLParseError()
