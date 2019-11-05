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
Extent pool interface.
"""

from .common.types import DS8K_POOL, DS8K_VOLUME, \
    DS8K_TSEREP, DS8K_ESEREP
from .common.base import Base, ReadOnlyManager
from .common.mixins import VolumeMixin
from pyds8k.exceptions import IDMissingError


# Note: VolumeMixin will override the methods with
# same name in RootResourceMixin.
class Pool(VolumeMixin, Base):
    # id_field = 'id'
    _template = {'id': '',
                 'name': '',
                 'node': '',
                 'stgtype': '',
                 'cap': '',
                 'capalloc': '',
                 'capavail': '',
                 'overprovisioned': '',
                 'easytier': '',
                 'tieralloc': [],
                 'threshold': '',
                 'real_capacity_allocated_on_ese': None,
                 'virtual_capacity_allocated_on_ese': None,
                 DS8K_VOLUME: '',
                 DS8K_TSEREP: '',
                 DS8K_ESEREP: '',
                 }
    related_resources_collection = (DS8K_VOLUME, DS8K_TSEREP, DS8K_ESEREP)

    def __repr__(self):
        return "<Extent Pool: {0}>".format(self._get_id())

    def get_tserep(self):
        if not self.id:
            raise IDMissingError()
        tserep = self.all(DS8K_TSEREP).list()
        self._start_updating()
        setattr(self, DS8K_TSEREP, tserep)
        self._stop_updating()
        return tserep

    def get_TSE_rep(self):
        return self.get_tserep()[0]

    def get_eserep(self):
        if not self.id:
            raise IDMissingError()
        eserep = self.all(DS8K_ESEREP).list()
        self._start_updating()
        setattr(self, DS8K_ESEREP, eserep)
        self._stop_updating()
        return eserep

    def get_ESE_rep(self):
        return self.get_eserep()[0]

    def delete_tserep(self):
        if not self.id:
            raise IDMissingError()
        return self.all(DS8K_TSEREP).delete()

    def delete_eserep(self):
        if not self.id:
            raise IDMissingError()
        return self.all(DS8K_ESEREP).delete()

    def update_tserep_cap(self, cap, captype=''):
        if not self.id:
            raise IDMissingError()
        return self.all(DS8K_TSEREP
                        ).update({'cap': cap, 'captype': captype})

    def update_eserep_cap(self, cap, captype=''):
        if not self.id:
            raise IDMissingError()
        return self.all(DS8K_ESEREP
                        ).update({'cap': cap, 'captype': captype})

    def update_tserep_threshold(self, threshold):
        if not self.id:
            raise IDMissingError()
        return self.all(DS8K_TSEREP
                        ).update({'threshold': threshold})

    def update_eserep_threshold(self, threshold):
        if not self.id:
            raise IDMissingError()
        return self.all(DS8K_ESEREP
                        ).update({'threshold': threshold})


class PoolManager(ReadOnlyManager):
    """
    Manage Extent Pool resources.
    """
    resource_class = Pool
    resource_type = DS8K_POOL


RESOURCE_TUPLE = (Pool, PoolManager)
