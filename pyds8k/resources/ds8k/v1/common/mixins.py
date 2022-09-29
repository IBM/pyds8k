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
        """
        Get DS8000 System Object

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.systems.System`.

        """
        return self.all(types.DS8K_SYSTEM, rebuild_url=True).list()


class RootNodeMixin(object):
    def get_nodes(self, node_id=None):
        """
        Get nodes

        Args:
            node_id (str): get the node by id or all nodes if no id specified.

        Returns:
            list:A list of :py:class:`pyds8k.resources.ds8k.v1.nodes.Node`.

        """
        if node_id:
            return self.get_node(node_id)
        return self.all(types.DS8K_NODE, rebuild_url=True).list()

    def get_node(self, node_id):
        """
        Get a node by id

        Args:
            node_id (str): id of the node to get.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.nodes.Node`.

        """
        return self.one(types.DS8K_NODE, node_id, rebuild_url=True).get()


class RootMarrayMixin(object):
    def get_marrays(self, marray_id=None):
        """
        Get managed arrays

        Args:
            marray_id (str): id of the target managed array, get all if none

        Returns:
            list: the list of
            :py:class:`pyds8k.resources.ds8k.v1.marrays.Marray`.

        """
        if marray_id:
            return self.get_marray(marray_id)
        return self.all(types.DS8K_MARRAY, rebuild_url=True).list()

    def get_marray(self, marray_id):
        """
        Get a managed array.

        Args:
            marray_id (str): Required. id of the target managed array.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.marrays.Marray`.

        """
        return self.one(types.DS8K_MARRAY, marray_id, rebuild_url=True).get()


class RootUserMixin(object):
    def get_users(self, user_name=None):
        """
        Get users.

        Args:
            user_name (str): name of the target user. get all if none.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.users.User`.

        """
        if user_name:
            return self.get_user(user_name)
        return self.all(types.DS8K_USER, rebuild_url=True).list()

    def get_user(self, user_name):
        """
        Get a user.

        Args:
            user_name (str): Required. the name of the target user.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.users.User`.

        """
        return self.one(types.DS8K_USER, user_name, rebuild_url=True).get()


class RootIOEnclosureMixin(object):
    def get_io_enclosures(self, enclosure_id=None):
        """
        Get IO Enclosures.

        Args:
            enclosure_id (str): id of the target IO Enclosure. Get all if none.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.io_enclosures.IOEnclosure`.

        """
        if enclosure_id:
            return self.get_io_enclosure(enclosure_id)
        return self.all(types.DS8K_IOENCLOSURE, rebuild_url=True).list()

    def get_io_enclosure(self, enclosure_id):
        """
        Get an IO Enclosure.

        Args:
            enclosure_id (str): Required. id of the target IO Enclosure.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.io_enclosures.IOEnclosure`.

        """
        return self.one(types.DS8K_IOENCLOSURE,
                        enclosure_id,
                        rebuild_url=True).get()


class RootEncryptionGroupMixin(object):
    def get_encryption_groups(self, group_id=None):
        """
        Get Encryption Groups.

        Args:
            group_id (str): id of the target Encryption Group. Get all if none.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.encryption_groups.EncryptionGroup`.

        """
        if group_id:
            return self.get_encryption_group(group_id)
        return self.all(types.DS8K_ENCRYPTION_GROUP, rebuild_url=True).list()

    def get_encryption_group(self, group_id):
        """
        Get An Encryption Groups.

        Args:
            group_id (str): Required. id of the target Encryption Group.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.encryption_groups.EncryptionGroup`.

        """
        return self.one(types.DS8K_ENCRYPTION_GROUP,
                        group_id,
                        rebuild_url=True).get()


class RootPoolMixin(object):
    def get_pools(self, pool_id=None):
        """
        Get Extent Pools

        Args:
            pool_id (str): id of the target extent pool. Get all if none.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.pools.Pool`.

        """
        if pool_id:
            return self.get_pool(pool_id)
        return self.all(types.DS8K_POOL, rebuild_url=True).list()

    def get_pool(self, pool_id):
        """
        Get Extent Pool

        Args:
            pool_id (str): Required. id of the target extent pool.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.pools.Pool`.

        """
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
        """
        Get volumes of a pool by the pool id.

        Args:
            pool_id (str): id of the target extent pool.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return self.one(types.DS8K_POOL,
                        pool_id,
                        rebuild_url=True
                        ).all(types.DS8K_VOLUME).list()


class RootResourceGroupMixin(object):
    def get_resource_groups(self, resource_group_id=None):
        """
        Get Resource Groups

        Args:
            resource_group_id (str): id of the target resource group.
                                     Get all if none.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.resource_groups.ResourceGroup`.

        """
        if resource_group_id:
            return self.get_resource_group(resource_group_id)
        return self.all(types.DS8K_RESOURCE_GROUP, rebuild_url=True).list()

    def get_resource_group(self, resource_group_id):
        """
        Get a Resource Group

        Args:
            resource_group_id (str): Required. id of the target resource group.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.resource_groups.ResourceGroup`.

        """
        return self.one(types.DS8K_RESOURCE_GROUP,
                        resource_group_id,
                        rebuild_url=True).get()

    def delete_resource_group(self, resource_group_id):
        """
        Delete a Resource Group

        Args:
            resource_group_id (str): Required. id of the target resource group.

        Returns:
            tuple: tuple of DS8000 Server Response.

        """
        return self.one(types.DS8K_RESOURCE_GROUP,
                        resource_group_id,
                        rebuild_url=True).delete()

    def create_resource_group(
            self,
            label,
            name='',
            resource_group_id='',):
        """
        Create one Resource Group

        Args:
            label (str): Required.
                        The label for the resource group to be created.
            name (str): The name for the resource group to be created.
            resource_group_id (str): The resource group id to be created.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.resource_groups.ResourceGroup`.

        """
        _, res = self.all(types.DS8K_RESOURCE_GROUP,
                          rebuild_url=True
                          ).posta({'label': label,
                                   'id': resource_group_id,
                                   'name': name,
                                   }
                                  )
        return res

    def update_resource_group(
            self,
            resource_group_id,
            label='',
            name='',
            cs_global='',
            pass_global='',
            gm_masters='',
            gm_sessions=''):
        """
        Update one Resource Group

        Args:
            resource_group_id (str): Required.
                                    The resource group id to be updated.
            label (str): The label to assign to the resource group.
            name (str): The name to assign to the resource group.
            cs_global (str): The resource group label to associate with the
                             Copy Services Global Resource Scope.
            pass_global (str): The resource group label to associate with the
                               Pass-thru Global Copy Services Resource Scope.
            gm_masters (list): An list of Global Mirror session IDs allowed
                               to be used as a master session for volumes
                               in this resource.
            gm_sessions (list): A list of Global Mirror session IDs allowed
                                to be used for the volumes in this resource.

        Returns:
            tuple: tuple of DS8000 Server Response.

        """
        _, res = self.one(types.DS8K_RESOURCE_GROUP,
                          resource_group_id,
                          rebuild_url=True).update({
                                'label': label,
                                'name': name,
                                'cs_global': cs_global,
                                'pass_global': pass_global,
                                'gm_masters': gm_masters,
                                'gm_sessions': gm_sessions,
                                }
                            )
        return res


class RootVolumeMixin(object):
    def get_volumes(self, volume_id=None):
        """
        Get Volumes

        Args:
            volume_id (str): id of the target volume. Get all if none.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        if volume_id:
            return self.get_volume(volume_id)
        return self.all(types.DS8K_VOLUME, rebuild_url=True).list()

    def get_volume(self, volume_id):
        """
        Get A volume.

        Args:
            volume_id (str): Required. id of the target volume.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return self.one(types.DS8K_VOLUME, volume_id, rebuild_url=True).get()

    def delete_volume(self, volume_id):
        """
        Delete A volume.

        Args:
            volume_id (str): Required. id of the target volume.

        Returns:
            tuple: tuple of DS8000 Server Response.

        """
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).delete()
        return res

    def create_volume(
            self,
            name,
            cap,
            pool,
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            captype=types.DS8K_CAPTYPE_GIB,
            lss='',
            tp='',
            id=''):
        """
        Create One Volume

        Args:
            name (str): Required. The name for the volume to be created
            cap (str): Required. The capacity, number in str
            pool (str): Required. The pool for the volume
            stgtype (str): select from types.DS8K_VOLUME_TYPES,
                          Default to ``'fb'``
            captype (str): select from types.DS8K_CAPTYPES,
                          Default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method,
                     valid options include `none`, `ese`, `tse`
            id (str): volume id to be created

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        self._verify_type(captype, types.DS8K_CAPTYPES)
        self._verify_type(stgtype, types.DS8K_VOLUME_TYPES)
        self._verify_type(tp, types.DS8K_TPS)
        _, res = self.all(types.DS8K_VOLUME,
                          rebuild_url=True
                          ).posta({'name': name,
                                   'cap': cap,
                                   'captype': captype,
                                   'stgtype': stgtype,
                                   'pool': pool,
                                   'lss': lss,
                                   'tp': tp,
                                   'id': id
                                   }
                                  )
        return res

    def create_volumes(
            self,
            name_col,
            cap,
            pool,
            name='',
            quantity='',
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            captype=types.DS8K_CAPTYPE_GIB,
            lss='',
            tp='',
            ids=None
    ):
        """
        Create a group of volumes with different names

        Args:
            name_col (list): ["name-1", "name-2",..., "name-N"]
            cap (str): the capacity, number in str
            pool (str): the pool for the volume
            name (str): Either 1) Name of the volume to be created,
                       or 2) Prefix of the <quantity> volumes to be created
            quantity (str): number of volumes to create, number in str
            stgtype (str): select from types.DS8K_VOLUME_TYPES,
                          default to ``'fb'``
            captype (str): select from types.DS8K_CAPTYPES,
                          default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method,
                     in ``none``, ``ese``, ``tse``
            ids (list): list of volume ids to be created.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        self._verify_type(captype, types.DS8K_CAPTYPES)
        self._verify_type(stgtype, types.DS8K_VOLUME_TYPES)
        self._verify_type(tp, types.DS8K_TPS)
        _, res = self.all(types.DS8K_VOLUME,
                          rebuild_url=True
                          ).posta({'name': name,
                                   'namecol': name_col if name_col else None,
                                   'quantity': quantity,
                                   'cap': cap,
                                   'captype': captype,
                                   'stgtype': stgtype,
                                   'pool': pool,
                                   'lss': lss,
                                   'tp': tp,
                                   'ids': ids
                                   }
                                  )
        return res

    def create_alias_volumes(
            self,
            id,
            ckd_base_ids,
            quantity='',
            alias_create_order='decrement'
    ):
        """
        Create ckd alias volumes for a list of base ckd volumes

        Args:
            id (str): the starting volume id for where aliases
                    should be created
            ckd_base_ids (list): list of ckd base ids aliases
                    will be created for
            quantity (str): number of aliases per ckd base id to
                    create, number in str
            alias_create_order (str): whether to ``increment``
                    or ``decrement`` from starting id
                    default ``decrement``
        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        _, res = self.all(types.DS8K_VOLUME,
                          rebuild_url=True
                          ).posta({'id': id,
                                   'quantity': quantity,
                                   'alias': 'true',
                                   'alias_create_order': alias_create_order,
                                   'ckd_base_ids': ckd_base_ids
                                   }
                                  )
        return res

    def create_volume_ckd(self, name, cap, pool,
                          captype='', lss='', tp='', id=''
                          ):
        """
        Create One CKD Volume

        Args:
            name (str): Required. The name for the volume to be created
            cap (str): Required. The capacity, number in str
            pool (str): Required. The pool for the volume
            captype (str): select from types.DS8K_CAPTYPES,
                          Default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method,
                     valid options include `none`, `ese`, `tse`
            id (str): volume id to be created

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return self.create_volume(
            name, cap, pool,
            stgtype=types.DS8K_VOLUME_TYPE_CKD,
            captype=captype,
            lss=lss,
            tp=tp,
            id=id
        )

    def create_volume_fb(self, name, cap, pool,
                         captype='', lss='', tp='', id=''
                         ):
        """
        Create One FB Volume

        Args:
            name (str): Required. The name for the volume
                       to be created
            cap (str): Required. The capacity, number in str
            pool (str): Required. The pool for the volume
            captype (str): select from types.DS8K_CAPTYPES,
                          Default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method,
                     valid options include `none`, `ese`, `tse`
            id (str): volume id to be created

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return self.create_volume(
            name, cap, pool,
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            captype=captype,
            lss=lss,
            tp=tp,
            id=id
        )

    def create_volumes_with_same_prefix(
            self,
            name,
            cap,
            pool,
            quantity='',
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            captype=types.DS8K_CAPTYPE_GIB,
            lss='',
            tp='',
            ids=None
    ):
        """
        Create a volume with a name or a group of
        volumes with the same prefix

        Args:
            name (str): 1, Name of the volume to be created,
                       or 2. Prefix of the <quantity> volumes
                       to be created
            cap (str): the capacity, number in str
            pool (str): the pool for the volume
            quantity (str): number of volumes to create, number in str
            stgtype (str): select from types.DS8K_VOLUME_TYPES,
                          default to ``'fb'``
            captype (str): select from types.DS8K_CAPTYPES,
                          default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method, in none, ese, tse
            ids (list): list of volume ids to be created

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return self.create_volumes(
            None, cap, pool,
            name=name,
            quantity=quantity,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            ids=ids
        )

    def create_volumes_without_same_prefix(
            self,
            name_col,
            cap,
            pool,
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            captype=types.DS8K_CAPTYPE_GIB,
            lss='',
            tp='',
            ids=None
    ):
        """
        Create a group of volumes with specified names

        Args:
            name_col (str): ["name-1", "name-2",..., "name-N"]
            cap (str): the capacity, number in str
            pool (str): the pool for the volume
            stgtype (str): select from types.DS8K_VOLUME_TYPES,
                          default to ``'fb'``
            captype (str): select from types.DS8K_CAPTYPES,
                         default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method, in none, ese, tse
            ids (list): list of volume ids to be created

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.
        """
        if not isinstance(name_col, list):
            raise ValueError(
                INVALID_TYPE.format('list')
            )
        return self.create_volumes(
            name_col, cap, pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            ids=ids
        )

    def create_volumes_with_names(
            self,
            names,
            cap,
            pool,
            stgtype=types.DS8K_VOLUME_TYPE_FB,
            captype=types.DS8K_CAPTYPE_GIB,
            lss='',
            tp='',
            ids=None
    ):
        """
        Create a group of volumes with specified names

        Args:
            names (str): ["name-1", "name-2",..., "name-N"]
            cap (str): the capacity, number in str
            pool (str): the pool for the volume
            stgtype (str): select from types.DS8K_VOLUME_TYPES,
                         default to ``'fb'``
            captype (str): select from types.DS8K_CAPTYPES,
                         default to ``'gib'``
            lss (str): logical subsystem id
            tp (str): storage allocation method, in none, ese, tse
            ids (list): list of volume ids to be created

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.
        """
        if not isinstance(names, list):
            raise ValueError(
                INVALID_TYPE.format('list')
            )
        return self.create_volumes(
            names, cap, pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            ids=ids
        )

    def update_volume_rename(self, volume_id, new_name):
        """
        Rename a volume by its id

        Args:
            volume_id (str): id of the volume
            new_name (str): the new name of the volume

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).update({'name': new_name})
        return res

    def update_volume_extend(self, volume_id, new_size, captype=''):
        """

        Args:
            volume_id (str): Required. id of the target volume.
            new_size (str): Required. new size of the target volume.
            captype (str): Required. select from types.DS8K_CAPTYPES.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        _, res = self.one(types.DS8K_VOLUME,
                          volume_id,
                          rebuild_url=True).update(
            {'cap': new_size, 'captype': captype}
        )
        return res

    def update_volume_move(self, volume_id, new_pool):
        """
        Move one volume to a new extent pool.
        Args:
            volume_id (str): Required. id of the target volume.
            new_pool (str): Required. id of the new extent pool.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
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
        """
        Get IO Ports

        Args:
            port_id (str): id of the target IO port. Get all if none.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.ioports.IOPort`.

        """
        if port_id:
            return self.get_ioport(port_id)
        return self.all(types.DS8K_IOPORT, rebuild_url=True).list()

    def get_ioport(self, port_id):
        """
        Get an IO Port.

        Args:
            port_id (str): Required. id of the target IO port.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.ioports.IOPort`.

        """
        return self.one(types.DS8K_IOPORT, port_id, rebuild_url=True).get()


class RootHostPortMixin(object):
    def get_host_ports(self, port_id=None):
        """
        Get Host Ports.

        Args:
            port_id (str): id of the target host port. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
        if port_id:
            return self.get_host_port(port_id)
        return self.all(types.DS8K_HOST_PORT, rebuild_url=True).list()

    def get_host_port(self, port_id):
        """
        Get A Host Port.
        Args:
            port_id (str): Required. id of the target host port.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
        return self.one(types.DS8K_HOST_PORT, port_id, rebuild_url=True).get()

    def delete_host_port(self, port_id):
        """
        Delete A Host Port.

        Args:
            port_id (str): Required. id of the target host port.

        Returns:
            tuple: A tuple of HTTP Response and DS8000 server message.

        """
        _, res = self.one(types.DS8K_HOST_PORT,
                          port_id,
                          rebuild_url=True
                          ).delete()
        return res

    def create_host_port(self, port_id, host_name):
        """
        Create A Host Port.

        Args:
            port_id (str): Required. wwpn of the port.
            host_name (str): Required. name of the host.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
        # .create().save() is not a good way for DS8K.
        _, res = self.all(types.DS8K_HOST_PORT,
                          rebuild_url=True
                          ).posta({'wwpn': port_id, 'host': host_name})
        return res

    def update_host_port_change_host(self, port_id, host_name):
        """
        Change Port to another Host.

        Args:
            port_id (str): Required. id of the host port.
            host_name (): Required. name of the new host.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
        _, res = self.one(types.DS8K_HOST_PORT,
                          port_id,
                          rebuild_url=True
                          ).update({'host': host_name})
        return res


class RootHostMixin(object):
    def get_hosts(self, host_name=None):
        """
        Get Hosts.

        Args:
            host_name (str): name of the target host. Get all if None.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.hosts.Host`.

        """
        if host_name:
            return self.get_host(host_name)
        return self.all(types.DS8K_HOST, rebuild_url=True).list()

    def get_host(self, host_name):
        """
        Get A Host.

        Args:
            host_name (str): Required. name of the target host.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.hosts.Host`.

        """
        return self.one(types.DS8K_HOST, host_name, rebuild_url=True).get()

    def get_ioports_by_host(self, host_name):
        """
        Get IO Ports by the name of the Host.
        Args:
            host_name (str): Required. name of the host.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.ioports.IOPort`.

        """
        return self.one(types.DS8K_HOST,
                        host_name,
                        rebuild_url=True
                        ).all(types.DS8K_IOPORT).list()

    def get_host_ports_by_host(self, host_name):
        """
        Get Host Ports by the name of the Host.

        Args:
            host_name (str): Required. name of the host.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
        return self.one(types.DS8K_HOST,
                        host_name,
                        rebuild_url=True
                        ).all(types.DS8K_HOST_PORT).list()

    def get_mappings_by_host(self, host_name):
        """
        Get Volume Mappings by the name fo the Host.

        Args:
            host_name (str): Required. name of the host.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.mappings.Volmap`.

        """
        return self.one(types.DS8K_HOST,
                        host_name,
                        rebuild_url=True
                        ).all(types.DS8K_VOLMAP).list()

    def get_mapping_by_host(self, host_name, lunid):
        """
        Get the Volume Mapping by the name of the host
        and the id of the volume.

        Args:
            host_name (str): Required. name of the host.
            lunid (str): Required. id of the volume.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.mappings.Volmap`.

        """
        return self.one(types.DS8K_HOST,
                        host_name,
                        rebuild_url=True
                        ).one(types.DS8K_VOLMAP, lunid).get()

    def get_volumes_by_host(self, host_name):
        """
        Get Volumes by the name of the Host.

        Args:
            host_name (str): Required. name of the host.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return (
            self.one(types.DS8K_HOST, host_name, rebuild_url=True)
            .all(types.DS8K_VOLUME)
            .list()
        )

    def delete_host(self, host_name):
        """
        Delete a host by name.

        Args:
            host_name (str): Required. name of the host.

        Returns:
            tuple: tuple of DS8000 Server Response.

        """
        _, res = self.one(types.DS8K_HOST,
                          host_name,
                          rebuild_url=True
                          ).delete()
        return res

    def create_host(self, host_name, hosttype):
        """
        Create A Host.

        Args:
            host_name (str): Required. name of the host.
            hosttype (str): Required. type of the host.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.hosts.Host`.

        """
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
        """
        Get LSS

        Args:
            lss_id (str): id of the target LSS. Get all if None.
            lss_type (str): type of the target LSS.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.lss.LSS`.

        """
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
        """
        Get LSS by id

        Args:
            lss_id (str): Required. id of the target LSS.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.lss.LSS`.

        """
        return self.one(types.DS8K_LSS, lss_id, rebuild_url=True).get()

    def get_volumes_by_lss(self, lss_id):
        """
        Get Volumes by id of the LSS

        Args:
            lss_id (str): Required. id of the LSS.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        return self.one(types.DS8K_LSS,
                        lss_id,
                        rebuild_url=True
                        ).all(types.DS8K_VOLUME).list()

    def create_lss_ckd(
            self,
            lss_id=None,
            lss_type=types.DS8K_VOLUME_TYPE_CKD,
            lcu_type=types.DS8K_LCU_TYPE_3990_6,
            ss_id=None):
        """
        Create CKD LSS

        Args:
            lss_id (str): Required. id of the lss to be created.
            lss_type (str): 'ckd', optional
            lcu_type (str): valid types are 3990-3, 3990-6, 3990-tpf, bs2000
            ss_id (str): associated subsystem id

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.lss.LSS`.

        """
        self._verify_type(lss_type, types.DS8K_LSS_TYPES)
        self._verify_type(lcu_type, types.DS8K_LCU_TYPES)
        _, res = self.all(
            types.DS8K_LSS,
            rebuild_url=True
        ).posta(
            {
                'id': lss_id,
                'type': lss_type,
                'sub_system_identifier': ss_id,
                'ckd_base_cu_type': lcu_type
            }
        )
        return res

    def delete_lss_by_id(self, lss_id):
        """
        Delete an LSS.

        Args:
            lss_id (str): Require. id of lss to be deleted.

        Returns:
            tuple: tuple of HTTP Response and DS8000 server message.

        """
        return self.one(types.DS8K_LSS, lss_id, rebuild_url=True).delete()


class RootFlashCopyMixin(object):
    def get_flashcopies(self, volume_id=None):
        """
        Get Flash Copies. Deprecated after R8.

        Args:
            volume_id (str):  id of the associating volume. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.flashcopy.FlashCopy`.

        """
        if not volume_id and self.resource_type == "volumes":
            volume_id = self.id

        if volume_id:
            return self.get_flashcopies_by_volume(volume_id)

        return self.all(types.DS8K_FLASHCOPY, rebuild_url=True).list()

    def get_flashcopy(self, volume_id=None):
        """
        Get A Flash Copy. Deprecated after R8.

        Args:
            volume_id (str): Required.  id of the associating volume.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.flashcopy.FlashCopy`.

        """
        return self.get_flashcopies(volume_id)

    def get_flashcopies_by_volume(self, volume_id):
        """
        Get Flash Copies by volume id. Deprecated after R8.

        Args:
            volume_id (str):  Required. id of the target volume.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.flashcopy.FlashCopy`.

        """
        return self.one(types.DS8K_VOLUME,
                        volume_id,
                        rebuild_url=True).all(types.DS8K_FLASHCOPY).list()

    def get_cs_flashcopies(self, fcid=None):
        """
        Get Copy Service Flash Copies(R8).
        Args:
            fcid (str): id of the flash copy. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.cs.flashcopies.FlashCopy`.

        """
        if fcid:
            return self.one('{}.{}'.format(
                types.DS8K_COPY_SERVICE_PREFIX,
                types.DS8K_CS_FLASHCOPY), fcid, rebuild_url=True).get()
        return self.all('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_FLASHCOPY), rebuild_url=True).list()

    def get_cs_flashcopy(self, fcid=None):
        """
        Get A Copy Service Flash Copy(R8).
        Args:
            fcid (str): Required. id of the flash copy.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.cs.flashcopies.FlashCopy`.

        """
        return self.get_cs_flashcopies(fcid)

    def create_cs_flashcopy(self, volume_pairs, options=[]):
        """
        Create Copy Service FlashCopy

        Args:
            volume_pairs (list):
            [{"source_volume": 0000,"target_volume": 1100},..]
            options (list): Options.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.cs.flashcopies.FlashCopy`.

        """
        for option in options:
            self._verify_type(option, types.DS8K_FC_OPTIONS)
        _, res = self.all('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_FLASHCOPY),
            rebuild_url=True).posta({"volume_pairs": volume_pairs,
                                     "options": options
                                     })
        return res

    def delete_cs_flashcopy(self, flashcopy_id):
        """
        Delete A Copy Service Flash Copy(R8).

        Args:
            flashcopy_id (str): Required. id of the target flash copy.

        Returns:
            tuple: A tuple of DS8000 RESTAPI server response.

        """
        _, res = self.one('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_FLASHCOPY),
            flashcopy_id,
            rebuild_url=True).delete()
        return res


class RootPPRCMixin(object):
    def get_pprc(self, pprc_id=None):
        """
        Get PPRC.

        Args:
            pprc_id (str): id of the PPRC. Get all if None.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.pprc.PPRC`.

        """
        if pprc_id:
            return self.one(types.DS8K_PPRC, pprc_id, rebuild_url=True).get()
        return self.all(types.DS8K_PPRC, rebuild_url=True).list()

    def get_pprc_by_volume(self, volume_id):
        """
        Get PPRC for a Volume by volume id.

        Args:
            volume_id (str): Required. id of the target volume.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.pprc.PPRC`.

        """
        return self.one(types.DS8K_VOLUME,
                        volume_id,
                        rebuild_url=True).all(types.DS8K_PPRC).list()

    def get_cs_pprcs(self, pprc_id=None):
        """
        Get Copy Service PPRCs(R8).

        Args:
            pprc_id (str): id of the PPRC. Get all if None.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.cs.pprcs.PPRC`.

        """
        if pprc_id:
            return self.get_cs_pprc(pprc_id)
        return self.all('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_PPRC), rebuild_url=True).list()

    def get_cs_pprc(self, pprc_id):
        """
        Get A Copy Service PPRCs(R8).

        Args:
            pprc_id (str): Required. id of the PPRC.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.cs.pprcs.PPRC`.

        """
        return self.one('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_PPRC), pprc_id, rebuild_url=True).get()


class RootEventMixin(object):
    def get_events(self, evt_id=None, evt_filter={}):
        """
        Get Events.

        Args:
            evt_id (str): id of the event. Get all if None.
            evt_filter (dict): predefined filters.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.events.Event`.

        """
        if evt_id:
            return self.get_event(evt_id)
        return self.all(types.DS8K_EVENT,
                        rebuild_url=True
                        ).list(params=evt_filter)

    def get_event(self, evt_id):
        """
        Get An Event.

        Args:
            evt_id (str): Required. id of the event.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.events.Event`.

        """
        return self.one(types.DS8K_EVENT, evt_id, rebuild_url=True).get()

    def get_events_by_filter(self,
                             warning=None,
                             error=None,
                             info=None,
                             before=None,
                             after=None,
                             ):
        """
        Get Events by filters.

        Args:
            warning (bool): True or False
            error (bool): True or False
            info (bool): True or False
            before (datetime): timestamp of the end of the time window.
            after (datetime): timestamp of the start of the time window.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.events.Event`.

        """
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
                        RootResourceGroupMixin,
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
        """
        Get Volumes for the Caller Object.

        Args:
            volume_id (str): id of the volume. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
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
        """
        Get A Volume for the Caller Object.

        Args:
            volume_id (str): Required. id of the volume.

        Returns:
            object: list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.volumes.Volume`.

        """
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_VOLUME, volume_id).get()


class FCPortMixin(object):
    def get_ioports(self, port_id=None):
        """
        Get IO Ports for the Caller Object.

        Args:
            port_id (str): id of the IO Port. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.ioports.IOPort`.

        """
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
        """
        Get An IO Port for the Caller Object.

        Args:
            port_id (str): Required. id of the IO Port.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.ioports.IOPort`.

        """
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_IOPORT, port_id).get()


class HostPortMixin(object):
    def get_host_ports(self, port_id=None):
        """
        Get Host Ports for the Caller Object.

        Args:
            port_id (str): id of the Host Port. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
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
        """
        Get An Host Ports for the Caller Object.

        Args:
            port_id (str): id of the Host Port. Get all if None.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.host_ports.HostPort`.

        """
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_HOST_PORT, port_id).get()


class FlashCopyMixin(object):
    def get_flashcopies(self, fcid=None):
        """
        Get Flash Copies for the Caller Object.

        Args:
            fcid (str): id of the flash copy. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.flashcopy.FlashCopy`.

        """
        if not self.id:
            raise IDMissingError()
        if fcid:
            return self.one(types.DS8K_FLASHCOPY, fcid).get()
        flashcopies = self.all(types.DS8K_FLASHCOPY).list()
        self._start_updating()
        setattr(self, types.DS8K_FLASHCOPY, flashcopies)
        self._stop_updating()
        return flashcopies

    def get_flashcopy(self, fcid):
        """
        Get A Flash Copies for the Caller Object.

        Args:
            fcid (str): Required. id of the flash copy.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.flashcopy.FlashCopy`.

        """
        return self.get_flashcopies(fcid)

    def get_cs_flashcopies(self, fcid=None):
        """
        Get Copy Service Flash Copies for the Caller Object.

        Args:
            fcid (str): id of the flash copy. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.cs.flashcopies.FlashCopy`.

        """
        if not self.id:
            raise IDMissingError()
        if fcid:
            return self.one('{}.{}'.format(
                types.DS8K_COPY_SERVICE_PREFIX,
                types.DS8K_CS_FLASHCOPY), fcid).get()
        flashcopies = self.all('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_FLASHCOPY)).list()
        self._start_updating()
        setattr(self, types.DS8K_CS_FLASHCOPY, flashcopies)
        self._stop_updating()
        return flashcopies

    def get_cs_flashcopy(self, fcid):
        """
        Get A Copy Service Flash Copies for the Caller Object.

        Args:
            fcid (str): Required. id of the flash copy.

        Returns:
            object:
            :py:class:`pyds8k.resources.ds8k.v1.cs.flashcopies.FlashCopy`.

        """
        return self.get_cs_flashcopies(fcid)


class PPRCMixin(object):
    def get_pprc(self, pprc_id=None):
        """
        Get PPRC for the Caller Object.

        Args:
            pprc_id (str): id of the PPRC. Get all if None.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.pprc.PPRC`.

        """
        if not self.id:
            raise IDMissingError()
        if pprc_id:
            return self.one(types.DS8K_PPRC, pprc_id).get()
        pprc = self.all(types.DS8K_PPRC).list()
        self._start_updating()
        setattr(self, types.DS8K_PPRC, pprc)
        self._stop_updating()
        return pprc

    def get_cs_pprcs(self, pprc_id=None):
        """
        Get Copy Service PPRC for the Caller Object.

        Args:
            pprc_id (str): id of the PPRC. Get all if None.

        Returns:
            list: A list of :py:class:`pyds8k.resources.ds8k.v1.cs.pprcs.PPRC`.

        """
        if not self.id:
            raise IDMissingError
        if pprc_id:
            return self.get_cs_pprc(pprc_id)
        pprcs = self.all('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_PPRC)).list()
        self._start_updating()
        setattr(self, '{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_PPRC), pprcs)
        self._stop_updating()
        return pprcs

    def get_cs_pprc(self, pprc_id):
        """
        Get A Copy Service PPRC for the Caller Object.

        Args:
            pprc_id (str): Required. id of the PPRC.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.cs.pprcs.PPRC`.

        """
        if not self.id:
            raise IDMissingError
        return self.one('{}.{}'.format(
            types.DS8K_COPY_SERVICE_PREFIX,
            types.DS8K_CS_PPRC), pprc_id).get()


class VolmapMixin(object):
    def get_mappings(self, lunid=None):
        """
        Get Mappings of the Volume by Volume id for the Caller Object.

        Args:
            lunid (str): id of the volume. Get all if None.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.mappings.Volmap`.

        """
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
        """
        Get the Mapping of the Volume by Volume id for the Caller Object.

        Args:
            lunid (str): Require. id of the volume.

        Returns:
            object: :py:class:`pyds8k.resources.ds8k.v1.mappings.Volmap`.

        """
        if not self.id:
            raise IDMissingError()
        return self.one(types.DS8K_VOLMAP, lunid).get()

    def delete_mapping(self, lunid):
        """
        Delete the Mapping of the Volume by Volume id for the Caller Object.

        Args:
            lunid (str): Require. id of the volume.

        Returns:
            tuple: tuple of DS8000 RESTAPI Server Response.

        """
        if not self.id:
            raise IDMissingError()
        _, res = self.one(types.DS8K_VOLMAP, lunid).delete()
        return res

    def create_mappings(self, volumes=[], mappings=[]):
        """
        Create the Mapping of the Volume by Volume id for the Caller Object.

        Args:
            volumes (list): Require. volume ids.
            mappings (list): Required. mappings.

        Returns:
            list: A list of
            :py:class:`pyds8k.resources.ds8k.v1.mappings.Volmap`.

        """
        if not self.id:
            raise IDMissingError()
        if volumes:
            _, res = self.all(types.DS8K_VOLMAP).posta({'volumes': volumes})
        else:
            _, res = self.all(types.DS8K_VOLMAP).posta({'mappings': mappings})
        return res
