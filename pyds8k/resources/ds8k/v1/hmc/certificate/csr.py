##############################################################################
# Copyright 2023 IBM Corp.
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
Hardware Management Console Certificate Signing Request interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta

from ...common.base import Base, BaseManager
from ...common.types import DS8K_HMC_CERTIFICATE_CSR


@six.add_metaclass(ResourceMeta)
class HmcCertificateCsr(Base):
    resource_type = DS8K_HMC_CERTIFICATE_CSR

    # id_field = ''

    # _template = {}

    # readonly_fields = {''}

    # related_resources_collection = ()

    # def __repr__(self):
    #     return "<HMC CSR: {0}>".format(self.id)


@six.add_metaclass(ManagerMeta)
class HmcCertificateCsrManager(BaseManager):
    """
    Manage Hardware Management Console Certificate Signing Request resources.
    """
    resource_class = HmcCertificateCsr
    resource_type = DS8K_HMC_CERTIFICATE_CSR

    def post(self, url='', body=None):
        return self._post(url=url, body=body)
