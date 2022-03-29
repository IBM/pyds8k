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
from pyds8k.httpclient import HTTPClient
from pyds8k.base import Resource, DefaultManager
from pyds8k.resources.ds8k.v1.systems import System, \
    SystemManager

logger = getLogger(PYDS8K_DEFAULT_LOGGER)
DEFAULT_PORT = 8452


class Client(object):
    """
    Top-level object to access all the DS8K resources.

    See available member functions from the docstring of
    :py:mod:`pyds8k.resources.ds8k.v1.common.mixins`

    Args:
        service_address (string): Required. Hostname/IP address
                    of the REST server if it is standalone or the
                    hostname/IP address of the DS8K system.
        user (string): Required. Username for logining to the
                     DS8K system.
        password (string): Required. Password for logining to
                     the DS8K system.
        port (int):  Port number of the server.
        hostname (string): Hostname/IP address of the DS8K HMC.
                     Required if the REST-API server is standalone.
        timeout (float): How long to wait for the server to send
                     data before giving up. In seconds.
                     Default is 25, and 0 means no limitation.
        verify (bool): Either 1)a boolean, indicating whether we verify
                       the server's TLS certificate,
                       or 2) a string of the path to a CA bundle to use.
                       Defaults to ``True``, meaning that the default CA of
                       python ``requests`` module is used.
                       The default CA bundle of requests module
                       can be found by:

                        | ``import requests``
                        | ``print(requests.certs.where())``
    Returns:
        object: DS8000 REST-API Client
    """

    def __init__(self, service_address, user, password,
                 port=DEFAULT_PORT,
                 hostname='',
                 service_type='ds8k',
                 service_version='v1',
                 timeout=None,
                 verify=True
                 ):
        logger.info('================== logger is enabled ==================')

        client = HTTPClient(service_address, user, password,
                            port=port,
                            hostname=hostname,
                            service_type=service_type,
                            service_version=service_version,
                            timeout=timeout,
                            verify=verify
                            )

        self.client = client
        self.resource = Resource(self.client, DefaultManager(self.client))
        self.system = System(self.client, SystemManager(self.client))

    def __getattr__(self, k):
        try:
            # if not self.system.is_loaded():
            #    self.system = self.system.get_system()
            method = getattr(self.system, k)
            if not callable(method):
                raise AttributeError(k)
            else:
                return method
        except Exception:
            raise AttributeError(k)
