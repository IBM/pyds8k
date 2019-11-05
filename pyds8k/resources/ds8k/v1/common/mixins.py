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

from datetime import datetime
from . import types
from pyds8k.messages import INVALID_TYPE
from pyds8k.exceptions import IDMissingError, \
    InvalidArgumentError
from pyds8k.dateutil import LocalTimezone

FORMAT = '%Y-%m-%dT%H:%M:%S%Z'


class RootBaseMixin(object):
    pass

# Note: the format of all the get list methods should be:
#           get_{right type in types}
#       the format of all the get single methods should be:
#           get_{singular_noun(right type in types)}
#       get_lss_by_id is get_pprc_by_id are special cases, because
#       lss and pprc do not have singular form.


class RootSystemMixin(object):
    def get_systems(self):
        return self.all(types.DS8K_SYSTEM, rebuild_url=True).list()


class RootNodeMixin(object):
    def get_nodes(self, node_id=None):
        if node_id:
            return self.get_node(node_id)
        return self.all(types.DS8K_NODE, rebuild_url=True).list()

    def get_node(self, node_id):
        return self.one(types.DS8K_NODE, node_id, rebuild_url=True).get()


class RootMarrayMixin(object):
    def get_marrays(self, marray_id=None):
        if marray_id:
            return self.get_marray(marray_id)
        return self.all(types.DS8K_MARRAY, rebuild_url=True).list()

    def get_marray(self, marray_id):
        return self.one(types.DS8K_MARRAY, marray_id, rebuild_url=True).get()


class RootUserMixin(object):
    def get_users(self, user_name=None):
        if user_name:
            return self.get_user(user_name)
        return self.all(types.DS8K_USER, rebuild_url=True).list()

    def get_user(self, user_name):
        return self.one(types.DS8K_USER, user_name, rebuild_url=True).get()


class RootIOEnclosureMixin(object):
    def get_io_enclosures(self, enclosure_id=None):
        if enclosure_id:
            return self.get_io_enclosure(enclosure_id)
        return self.all(types.DS8K_IOENCLOSURE, rebuild_url=True).list()

    def get_io_enclosure(self, enclosure_id):
        return self.one(types.DS8K_IOENCLOSURE,
                        enclosure_id,
                        rebuild_url=True).get()


class RootEncryptionGroupMixin(object):
    def get_encryption_groups(self, group_id=None):
        if group_id:
            return self.get_encryption_group(group_id)
        return self.all(types.DS8K_ENCRYPTION_GROUP, rebuild_url=True).list()

    def get_encryption_group(self, group_id):
        return self.one(types.DS8K_ENCRYPTION_GROUP,
                        group_id,
                        rebuild_url=True).get()


class RootPoolMixin(object):
    def get_pools(self, pool_id=None):
        if pool_id:
            return self.get_pool(pool_id)
        return self.all(types.DS8K_POOL, rebuild_url=True).list()

    def get_pool(self, pool_id):
        return self.one(types.DS8K_POOL, pool_id, rebuild_url=True).get()

    def get_tserep_by_pool(self, pool_id):
        return self.one(types.DS8K_POOL,
                        pool_id,
                        rebuild_url=True
                        ).all(types.DS8K_TSEREP).get()

    def get_eserep_by_pool(self, pool_id):
        return self.one(types.DS8K_POOL,
                        pool_id,
                        rebuild_url=True
                        ).all(types.DS8K_ESEREP).get()

    def delete_tserep_by_pool(self, pool_id):
        _, res = self.one(types.DS8K_POOL,
                          pool_id,
                          rebuild_url=True
                          ).all(types.DS8K_TSEREP).delete()
        return res

    def delete_eserep_by_pool(self, pool_id):
        _, res = self.one(types.DS8K_POOL,
                          pool_id,
                          rebuild_url=True
                          ).all(types.DS8K_ESEREP).delete()
        return res

    def update_tserep_cap_by_pool(self, pool_id, cap, captype=''):
        _, res = self.one(types.DS8K_POOL,
                          pool_id,
                          rebuild_url=True
                          ).all(
                              types.DS8K_TSEREP
                              ).update({'cap': cap, 'captype': captype})
        return res

    def update_eserep_cap_by_pool(self, pool_id, cap, captype=''):
        _, res = self.one(types.DS8K_POOL,
                          pool_id,
                          rebuild_url=True
                          ).all(
                              types.DS8K_ESEREP
                              ).update({'cap': cap, 'captype': captype})
        return res

    def update_tserep_threshold_by_pool(self, pool_id, threshold):
        _, res = self.one(types.DS8K_POOL,
                          pool_id,
                          rebuild_url=True
                          ).all(
                              types.DS8K_TSEREP
                              ).update({'threshold': threshold})
        return res

    def update_eserep_threshold_by_pool(self, pool_id, threshold):
        _, res = self.one(types.DS8K_POOL,
                          pool_id,
                          rebuild_url=True
                          ).all(
                              types.DS8K_ESEREP
                              ).update({'threshold': threshold})
        return res

    def get_volumes_by_pool(self, pool_id):
        return self.one(types.DS8K_POOL,
                        pool_id,
                        rebuild_url=True
                        ).all(types.DS8K_VOLUME).list()


class RootVolumeMixin(object):
    def get_volumes(self, volume_id=None):
        if volume_id:
            return self.get_volume(volume_id)
        return self.all(types.DS8K_VOLUME, rebuild_url=True).list()

    def get_volume(self, volume_id):
        return self.one(types.DS8K_VOLUME, volume_id, rebuild_url=True).get()

    def delete_volume(self, volume_id):
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).delete()
        return res

    def create_volume(self, name, cap, pool, stgtype,
                      captype='', lss='', tp='',
                      ):
        self._verify_type(captype, types.DS8K_CAPTYPES)
        self._verify_type(stgtype, types.DS8K_VOLUME_TYPES)
        self._verify_type(tp, types.DE8K_TPS)
        _, res = self.all(types.DS8K_VOLUME,
                          rebuild_url=True
                          ).posta({'name': name,
                                   'cap': cap,
                                   'captype': captype,
                                   'stgtype': stgtype,
                                   'pool': pool,
                                   'lss': lss,
                                   'tp': tp,
                                   }
                                  )
        return res

    def create_volumes(self, cap, pool, stgtype,
                       name='', quantity='',
                       name_col='',
                       captype='', lss='', tp='',
                       ):
        self._verify_type(captype, types.DS8K_CAPTYPES)
        self._verify_type(stgtype, types.DS8K_VOLUME_TYPES)
        self._verify_type(tp, types.DE8K_TPS)
        _, res = self.all(types.DS8K_VOLUME,
                          rebuild_url=True
                          ).posta({'name': name,
                                   'namecol': name_col,
                                   'quantity': quantity,
                                   'cap': cap,
                                   'captype': captype,
                                   'stgtype': stgtype,
                                   'pool': pool,
                                   'lss': lss,
                                   'tp': tp,
                                   }
                                  )
        return res

    def create_volume_ckd(self, name, cap, pool,
                          captype='', lss='', tp='',
                          ):
        return self.create_volume(name=name, cap=cap,
                                  pool=pool,
                                  stgtype=types.DS8K_VOLUME_TYPE_CKD,
                                  captype=captype, lss=lss, tp=tp)

    def create_volume_fb(self, name, cap, pool,
                         captype='', lss='', tp='',
                         ):
        return self.create_volume(name=name, cap=cap,
                                  pool=pool, stgtype=types.DS8K_VOLUME_TYPE_FB,
                                  captype=captype, lss=lss, tp=tp)

    def create_volumes_with_same_prefix(self, cap, pool, stgtype,
                                        name='', quantity='',
                                        captype='', lss='', tp='',
                                        ):
        return self.create_volumes(cap=cap, pool=pool, stgtype=stgtype,
                                   name=name, quantity=quantity,
                                   captype=captype, lss=lss, tp=tp,
                                   )

    def create_volumes_without_same_prefix(self, cap, pool, stgtype,
                                           name_col='',
                                           captype='', lss='', tp='',
                                           ):
        return self.create_volumes(cap=cap, pool=pool, stgtype=stgtype,
                                   name_col=name_col,
                                   captype=captype, lss=lss, tp=tp,
                                   )

    def update_volume_rename(self, volume_id, new_name):
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).update({'name': new_name})
        return res

    def update_volume_extend(self, volume_id, new_size, captype=''):
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).update(
                              {'cap': new_size, 'captype': captype}
                              )
        return res

    def update_volume_move(self, volume_id, new_pool):
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).update({'pool': new_pool})
        return res

    # def update_volume_map(self, volume_id, host):
    #    _, res = self.one(types.DS8K_VOLUME,
    #                      volume_id,
    #                      rebuild_url=True).update({'host': host})
    #    return res


class RootIOPortMixin(object):
    def get_ioports(self, port_id=None):
        if port_id:
            return self.get_ioport(port_id)
        return self.all(types.DS8K_IOPORT, rebuild_url=True).list()

    def get_ioport(self, port_id):
        return self.one(types.DS8K_IOPORT, port_id, rebuild_url=True).get()


class RootHostPortMixin(object):
    def get_host_ports(self, port_id=None):
        if port_id:
            return self.get_host_port(port_id)
        return self.all(types.DS8K_HOST_PORT, rebuild_url=True).list()

    def get_host_port(self, port_id):
        return self.one(types.DS8K_HOST_PORT, port_id, rebuild_url=True).get()

    def delete_host_port(self, port_id):
        _, res = self.one(types.DS8K_HOST_PORT,
                          port_id,
                          rebuild_url=True
                          ).delete()
        return res

    def create_host_port(self, port_id, host_name):
        # .create().save() is not a good way for DS8K.
        _, res = self.all(types.DS8K_HOST_PORT,
                          rebuild_url=True
                          ).posta({'wwpn': port_id, 'host': host_name})
        return res

    def update_host_port_change_host(self, port_id, host_name):
        _, res = self.one(types.DS8K_HOST_PORT,
                          port_id,
                          rebuild_url=True
                          ).update({'host': host_name})
        return res


class RootHostMixin(object):
    def get_hosts(self, host_name=None):
        if host_name:
            return self.get_host(host_name)
        return self.all(types.DS8K_HOST, rebuild_url=True).list()

    def get_host(self, host_name):
        return self.one(types.DS8K_HOST, host_name, rebuild_url=True).get()

    def get_mappings_by_host(self, host_name):
        return self.one(types.DS8K_HOST,
                        host_name,
                        rebuild_url=True
                        ).all(types.DS8K_VOLMAP).list()

    def get_mapping_by_host(self, host_name, lunid):
        return self.one(types.DS8K_HOST,
                        host_name,
                        rebuild_url=True
                        ).one(types.DS8K_VOLMAP, lunid).get()

    def delete_host(self, host_name):
        _, res = self.one(types.DS8K_HOST,
                          host_name,
                          rebuild_url=True
                          ).delete()
        return res

    def create_host(self, host_name, hosttype):
        # .create().save() is not a good way for DS8K.
        _, res = self.all(types.DS8K_HOST,
                          rebuild_url=True
                          ).posta({'name': host_name, 'hosttype': hosttype})
        return res

    def update_host_add_ioports_all(self, host_name):
        _, res = self.one(types.DS8K_HOST,
                          host_name,
                          rebuild_url=True
                          ).update({'ioports': 'all'})
        return res

    def update_host_rm_ioports_all(self, host_name):
        _, res = self.one(types.DS8K_HOST,
                          host_name,
                          rebuild_url=True
                          ).update({'ioports': []})
        return res

    def map_volume_to_host(self, host_name, volume_id, lunid=''):
        post_data = {'mappings': [{lunid: volume_id}, ]} \
            if lunid else {'volumes': [volume_id]}
        _, res = self.one(types.DS8K_HOST,
                          host_name,
                          rebuild_url=True
                          ).all(types.DS8K_VOLMAP).posta(
                              post_data
                              )
        return res

    def unmap_volume_from_host(self, host_name, lunid):
        _, res = self.one(types.DS8K_HOST,
                          host_name,
                          rebuild_url=True
                          ).one(types.DS8K_VOLMAP, lunid).delete()
        return res


class RootLSSMixin(object):
    def get_lss(self, lss_id=None, lss_type=''):
        if lss_id:
            return self.get_lss_by_id(lss_id)
        if not lss_type:
            return self.all(types.DS8K_LSS, rebuild_url=True).list()
        elif str(lss_type) not in types.DS8K_VOLUME_TYPES:
            raise ValueError(
                INVALID_TYPE.format(
                    ', '.join(types.DS8K_VOLUME_TYPES)
                    )
                )
        return self.all(types.DS8K_LSS, rebuild_url=True).list(
            params={'type': lss_type}
        )

    def get_lss_by_id(self, lss_id):
        return self.one(types.DS8K_LSS, lss_id, rebuild_url=True).get()

    def get_volumes_by_lss(self, lss_id):
        return self.one(types.DS8K_LSS,
                        lss_id,
                        rebuild_url=True
                        ).all(types.DS8K_VOLUME).list()


class RootFlashCopyMixin(object):
    def get_flashcopies(self, fcid=None):
        return self.get_flashcopy(fcid)

    def get_flashcopy(self, fcid=None):
        if fcid:
            return self.one(types.DS8K_FLASHCOPY, fcid, rebuild_url=True).get()
        return self.all(types.DS8K_FLASHCOPY, rebuild_url=True).list()

    def get_flashcopies_by_volume(self, volume_id):
        return self.one(types.DS8K_VOLUME,
                        volume_id,
                        rebuild_url=True).all(types.DS8K_FLASHCOPY).list()


class RootPPRCMixin(object):
    def get_pprc(self, pprc_id=None):
        if pprc_id:
            return self.one(types.DS8K_PPRC, pprc_id, rebuild_url=True).get()
        return self.all(types.DS8K_PPRC, rebuild_url=True).list()

    def get_pprc_by_volume(self, volume_id):
        return self.one(types.DS8K_VOLUME,
                        volume_id,
                        rebuild_url=True).all(types.DS8K_PPRC).list()


class RootEventMixin(object):
    def get_events(self, evt_id=None, evt_filter={}):
        if evt_id:
            return self.get_event(evt_id)
        return self.all(types.DS8K_EVENT,
                        rebuild_url=True
                        ).list(params=evt_filter)

    def get_event(self, evt_id):
        return self.one(types.DS8K_EVENT, evt_id, rebuild_url=True).get()

    def get_events_by_filter(self,
                             warning=None,
                             error=None,
                             info=None,
                             before=None,
                             after=None,
                             ):
        severity = []
        for k, v in {'warning': warning,
                     'error': error,
                     'info': info,
                     }.items():
            if v:
                severity.append(k)

        evt_filter = {}
        if severity:
            evt_filter['severity'] = ','.join(severity)
        for k, v in {'before': before,
                     'after': after,
                     }.items():
            if v:
                if not isinstance(v, datetime):
                    raise InvalidArgumentError(
                        'before/after must be an datetime instance.'
                        )
                dttz = datetime(year=v.year,
                                month=v.month,
                                day=v.day,
                                hour=v.hour,
                                minute=v.minute,
                                second=v.second,
                                tzinfo=LocalTimezone(),
                                )
                evt_filter[k] = dttz.strftime(FORMAT)
        return self.get_events(evt_filter=evt_filter)


class RootResourceMixin(RootSystemMixin,
                        RootFlashCopyMixin,
                        RootPPRCMixin,
                        RootNodeMixin,
                        RootMarrayMixin,
                        RootUserMixin,
                        RootIOEnclosureMixin,
                        RootEncryptionGroupMixin,
                        RootEventMixin,
                        RootPoolMixin,
                        RootVolumeMixin,
                        RootLSSMixin,
                        RootIOPortMixin,
                        RootHostPortMixin,
                        RootHostMixin,
                        RootBaseMixin
                        ):
    pass


class VolumeMixin(object):
    def get_volumes(self, volume_id=None):
        if volume_id:
            return self.get_volume(volume_id)
        if not self.id:
            raise IDMissingError()
        volumes = self.all(types.DS8K_VOLUME).list()
        self._start_updating()
        setattr(self, types.DS8K_VOLUME, volumes)
        self._stop_updating()
        return volumes

    def get_volume(self, volume_id):
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_VOLUME, volume_id).get()


class FCPortMixin(object):
    def get_ioports(self, port_id=None):
        if port_id:
            return self.get_ioport(port_id)
        if not self.id:
            raise IDMissingError()
        ioports = self.all(types.DS8K_IOPORT).list()
        self._start_updating()
        setattr(self, types.DS8K_IOPORT, ioports)
        self._stop_updating()
        return ioports

    def get_ioport(self, port_id):
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_IOPORT, port_id).get()


class HostPortMixin(object):
    def get_host_ports(self, port_id=None):
        if port_id:
            return self.get_host_port(port_id)
        if not self.id:
            raise IDMissingError()
        host_ports = self.all(types.DS8K_HOST_PORT).list()
        self._start_updating()
        setattr(self, types.DS8K_HOST_PORT, host_ports)
        self._stop_updating()
        return host_ports

    def get_host_port(self, port_id):
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_HOST_PORT, port_id).get()


class FlashCopyMixin(object):
    def get_flashcopies(self, fcid=None):
        return self.get_flashcopy(fcid)

    def get_flashcopy(self, fcid=None):
        if not self.id:
            raise IDMissingError()
        if fcid:
            return self.one(types.DS8K_FLASHCOPY, fcid).get()
        flashcopies = self.all(types.DS8K_FLASHCOPY).list()
        self._start_updating()
        setattr(self, types.DS8K_FLASHCOPY, flashcopies)
        self._stop_updating()
        return flashcopies


class PPRCMixin(object):
    def get_pprc(self, pprc_id=None):
        if not self.id:
            raise IDMissingError()
        if pprc_id:
            return self.one(types.DS8K_PPRC, pprc_id).get()
        pprc = self.all(types.DS8K_PPRC).list()
        self._start_updating()
        setattr(self, types.DS8K_PPRC, pprc)
        self._stop_updating()
        return pprc


class VolmapMixin(object):
    def get_mappings(self, lunid=None):
        if lunid:
            return self.get_mapping(lunid)
        if not self.id:
            raise IDMissingError()
        mappings = self.all(types.DS8K_VOLMAP).list()
        self._start_updating()
        setattr(self, types.DS8K_VOLMAP, mappings)
        self._stop_updating()
        return mappings

    def get_mapping(self, lunid):
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_VOLMAP, lunid).get()

    def delete_mapping(self, lunid):
        if not self.id:
            raise IDMissingError()
        _, res = self.one(types.DS8K_VOLMAP, lunid).delete()
        return res

    def create_mappings(self, volumes=[], mappings=[]):
        if not self.id:
            raise IDMissingError()
        if volumes:
            _, res = self.all(types.DS8K_VOLMAP).posta({'volumes': volumes})
        else:
            _, res = self.all(types.DS8K_VOLMAP).posta({'mappings': mappings})
        return res
