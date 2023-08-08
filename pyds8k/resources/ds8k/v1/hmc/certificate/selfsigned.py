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
Hardware Management Console Self-signed Certificate interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta

from ...common.base import Base, BaseManager
from ...common.types import DS8K_HMC_CERTIFICATE_SELFSIGNED


@six.add_metaclass(ResourceMeta)
class HmcCertificateSelfSigned(Base):
    resource_type = DS8K_HMC_CERTIFICATE_SELFSIGNED


@six.add_metaclass(ManagerMeta)
class HmcCertificateSelfSignedManager(BaseManager):
    """
    Manage Hardware Management Console Self-signed Certificate resources.
    """
    resource_class = HmcCertificateSelfSigned
    resource_type = DS8K_HMC_CERTIFICATE_SELFSIGNED

    def post(self, url='', body=None):
        return self._post(url=url, body=body)
