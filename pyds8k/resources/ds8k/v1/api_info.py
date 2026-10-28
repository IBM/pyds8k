##############################################################################
# Copyright 2026 IBM Corp.
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
API information interface.
"""

from .common.base import ReadOnlyManager, SingletonBase
from .common.types import DS8K_API_INFO


class ApiInfo(SingletonBase):
    resource_type = DS8K_API_INFO
    _template = {
        'bundle_version': '',
    }

    def _add_base_to_url(self, url):
        # The API info lives at the API root, not under a resource route.
        return f'{self.client.service_address}/'

    def __repr__(self):
        return f"<ApiInfo: {self.bundle_version}>"


class ApiInfoManager(ReadOnlyManager):
    """
    Manage API information resources.
    """

    resource_class = ApiInfo
    resource_type = DS8K_API_INFO
