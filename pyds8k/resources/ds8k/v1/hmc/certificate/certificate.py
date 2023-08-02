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
Hardware Management Console Certificate interface.
"""
import six
from pyds8k.base import ManagerMeta, ResourceMeta

from ...common.base import Base, BaseManager
from ...common.types import DS8K_HMC_CERTIFICATE


@six.add_metaclass(ResourceMeta)
class HmcCertificate(Base):
    resource_type = DS8K_HMC_CERTIFICATE

    # id_field = ''

    # _template = {}

    # readonly_fields = {''}

    # related_resources_collection = ()

    # def __repr__(self):
    #     return "<HMC Certificate: {0}>".format(self.id)


@six.add_metaclass(ManagerMeta)
class HmcCertificateManager(BaseManager):
    """
    Manage Hardware Management Console Certificate resources.
    """
    resource_class = HmcCertificate
    resource_type = DS8K_HMC_CERTIFICATE

    # CAVEAT: Meta classes are built using the dir structure and the resulting
    # url is /hmc/certificate/certificate.
    # Force the default to be the correct url.
    def post(self, url='/hmc/certificate', body=None):
        files = {'file': body}
        # CAVEAT: self._post() underlying code from _post in
        # BaseManager -> Manager expects the body to be json.
        # Call the client directly, which calls requests.
        # Side effect is the REQ not being logged correctly.
        return self.client.post(url=url, files=files)
