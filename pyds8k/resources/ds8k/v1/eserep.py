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

"""
ESE Rep interface.
"""
from pyds8k.base import ManagerMeta, ResourceMeta
from .common.types import DS8K_ESEREP
from .common.base import SingletonBase, SingletonBaseManager
from .pools import Pool, PoolManager


class ESERep(SingletonBase, metaclass=ResourceMeta):
    resource_type = DS8K_ESEREP
    # id_field = 'id'
    _template = {'cap': '',
                 'capalloc': '',
                 'capavail': '',
                 'overprovisioned': '',
                 'threshold': '',
                 'pool': '',
                 }
    readonly_fileds = ('capalloc', 'capavail', 'overprovisioned', 'pool')
    related_resource = {'_pool': (Pool, PoolManager),
                        }

    def __getattr__(self, key):
        if key == 'id' or key == self.id_field:
            return 'eserep_in_pool_{}'.format(self.pool)
        return super(ESERep, self).__getattr__(key)


class ESERepManager(SingletonBaseManager, metaclass=ManagerMeta):
    """
    Manage ESE Rep resources.
    """
    resource_class = ESERep
    resource_type = DS8K_ESEREP

    def put(self, url='', body=None):
        return self._put(url=url, body=body)

    def patch(self, url='', body=None):
        return self._patch(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)
