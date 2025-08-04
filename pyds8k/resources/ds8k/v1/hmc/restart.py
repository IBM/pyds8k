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
Hardware Management Console Restart interface.
"""

from pyds8k.base import ManagerMeta, ResourceMeta
from pyds8k.resources.ds8k.v1.common.base import Base, BaseManager
from pyds8k.resources.ds8k.v1.common.types import DS8K_HMC_RESTART


class HMCRestart(Base, metaclass=ResourceMeta):
    resource_type = DS8K_HMC_RESTART


class HMCRestartManager(BaseManager, metaclass=ManagerMeta):
    """
    Manage Hardware Management Console Restart.
    """

    resource_class = HMCRestart
    resource_type = DS8K_HMC_RESTART

    def post(self, url='', body=None):
        return self._post(url=url, body=body)
