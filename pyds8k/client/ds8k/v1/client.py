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
from pyds8k.resources.ds8k.v1.common import types
from pyds8k.resources.ds8k.v1.systems import System, \
    SystemManager

logger = getLogger(PYDS8K_DEFAULT_LOGGER)
DEFAULT_PORT = 8452


class Client(object):
    """
    Top-level object to access all the DS8K resources.

    :param service_address: Hostname/IP address of the REST server if it is
                           standalone or the hostname/IP address of the DS8K
                           system. Required.
    :type service_address: string
    :param user: Username for logining to the DS8K system. Required.
    :type user: string
    :param password: Password for logining to the DS8K system. Required.
    :type password: string
    :param port: Port number of the server.
    :type port: int
    :param hostname: Hostname/IP address of the DS8K system. It is required if
                     the server is standalone.
    :type hostname: string
    :param timeout: How long to wait for the server to send data before giving
                    up. In seconds.
                    Default is 25, and 0 means no limitation.
    :type timeout: float
    """

    def __init__(self, service_address, user, password,
                 port=DEFAULT_PORT,
                 hostname='',
                 service_type='ds8k',
                 service_version='v1',
                 timeout=None,
                 ):
        logger.info('================== logger is enabled ==================')

        client = HTTPClient(service_address, user, password,
                            port=port,
                            hostname=hostname,
                            service_type=service_type,
                            service_version=service_version,
                            timeout=timeout,
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

    def create_volume(self, name, cap, pool, tp='', lss=''):
        """
        Create a fb volume.

        name, cap(in GiB) and pool id is mandatory.
        tp have three optional values: 'none', 'ese' and 'tse'.
        default is 'none', will create a standard volume.
        """

        return self.system.create_volume_fb(
            name=name, cap=cap,
            pool=pool, tp=tp,
            captype=types.DS8K_CAPTYPE_GIB,
            lss=lss,
        )

    def create_volumes(self, name_col, cap, pool, tp='', lss=''):
        """
        Create fb volumes.

        name_col, cap(in GiB) and pool id is mandatory.
        name_col is a volume name list.
        tp have three optional values: 'none', 'ese' and 'tse'.
        default is 'none', will create standard volumes.
        """

        return self.create_volumes_without_same_prefix(name_col, cap,
                                                       pool, tp, lss
                                                       )

    def create_volumes_with_same_prefix(self, name, cap, pool,
                                        quantity='', tp='', lss=''
                                        ):
        """
        Create fb volumes with same name prefix.

        name, cap(in GiB) pool id and quantity is mandatory.
        name is the volume name prefix, the final volume names will
        be something like 'prefix_1', 'prefix_2', ...
        tp have three optional values: 'none', 'ese' and 'tse'.
        default is 'none', will create standard volumes.
        """

        return self.system.create_volumes_with_same_prefix(
            cap=cap, pool=pool,
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            name=name, quantity=quantity,
            captype=types.DS8K_CAPTYPE_GIB, tp=tp,
            lss=lss,
        )

    def create_volumes_without_same_prefix(self, name_col, cap, pool,
                                           tp='', lss=''):
        return self.system.create_volumes_without_same_prefix(
            cap=cap, pool=pool,
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            name_col=name_col,
            captype=types.DS8K_CAPTYPE_GIB, tp=tp,
            lss=lss,
        )
