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

from functools import wraps, partial
from logging import getLogger
from contextlib import contextmanager
import unittest
from nose.tools import nottest
from datetime import datetime
from pyds8k import PYDS8K_DEFAULT_LOGGER
from pyds8k.utils import res_timer_recorder
from pyds8k.client.ds8k.v1.client import Client
from pyds8k.client.ds8k.v1.sc_client import SCClient
from pyds8k.resources.ds8k.v1.common import types
from pyds8k.size_converter import convert_size_gib_to_bytes

from .device import ds44 as ds8k_device

logger = getLogger(PYDS8K_DEFAULT_LOGGER)


def add_logger(route):
    def add_logger_deco(func):
        @wraps(func)
        def inner(self, route_id=None):
            if route_id:
                logger.info(
                    'Starting GET /{}/{} request'.format(route,
                                                         route_id
                                                         )
                    )
                res = func(self, route_id)
                logger.info(
                    'Successfully got {}: {}, detail is: {}'.format(
                        route,
                        res,
                        res.representation
                        )
                    )
                logger.info('Finish GET /{}/{} request'.format(route, res.id))
            else:
                logger.info('Starting GET /{} request'.format(route))
                res = func(self)
                logger.info(
                    'Successfully got {} {}: {}'.format(len(res),
                                                        route,
                                                        res,
                                                        )
                    )
                logger.info('Finish GET /{} request'.format(route))
            return res
        return inner
    return add_logger_deco


class TestIntegration(unittest.TestCase):

    @classmethod
    def setup_class(cls):

        cls.client = Client(ds8k_device.ipaddr,
                            ds8k_device.username, ds8k_device.password,
                            # hostname='mtc032h.tuc.stglabs.ibm.com',
                            port=ds8k_device.port,
                            )

    def __getattr__(self, k):
        if k.startswith('get_'):
            _, route = str(k).split('_', 1)

            @add_logger(route=route)
            def route_getter(self, route_id=None):
                return getattr(self.client, k)(route_id)
            return partial(route_getter, self)

        return super(TestIntegration, self).__getattr__(k)

    def test_system(self):
        logger.info('Starting GET /systems request')
        sys = self.client.get_system()
        logger.info(
            'Successfully got system: {}, detail is: {}'.format(
                sys,
                sys.representation
                )
            )
        logger.info('Finish GET /systems request')

    def test_nodes(self):
        nodes = self.get_nodes()
        self.get_nodes(nodes[0].id)

    def test_marrays(self):
        marrays = self.get_marrays()
        self.get_marrays(marrays[0].id)

    def test_lss(self):
        lss_list = self.get_lss()
        for l in lss_list:
            lss = self.get_lss(l.id)
            volumes = self._get_volumes_by(types.DS8K_LSS, lss)
            if volumes:
                self.get_volumes(volumes[0].id)
                return

    def test_ioports(self):
        ios = self.get_ioports()
        self.get_ioports(ios[0].id)

    def test_flashcopy(self):
        self.get_flashcopy()

        volume = self.get_volumes('0000')
        self._get_sub_resource_by(types.DS8K_VOLUME, volume,
                                  types.DS8K_FLASHCOPY
                                  )

    def test_pprc(self):
        self.get_pprc()

        volume = self.get_volumes('0000')
        self._get_sub_resource_by(types.DS8K_VOLUME, volume,
                                  types.DS8K_PPRC
                                  )

    def test_events(self):
        sys = self.client.get_system()
        before = datetime.now()
        after = datetime(year=before.year,
                         month=before.month,
                         day=before.day)
        logger.info('Starting GET /events request')
        events = sys.get_events_by_filter(warning=True,
                                          error=True,
                                          before=before,
                                          after=after)
        logger.info(
            'Successfully got {} events'.format(len(events))
            )
        logger.info('Finish GET /events request')

    def test_pools(self):
        pools = self.get_pools()
        for p in pools:
            pool = self.get_pools(p.id)
            vols = self._get_volumes_by(types.DS8K_POOL, pool)
            if vols:
                return

    # Skipped, because get all volumes is not allowed.
    @nottest
    def test_volumes(self):
        volumes = self.get_volumes()
        self.get_volumes(volumes[0].id)

    def test_volume(self):
        self.get_volumes('0000')

    def test_hosts(self):
        hosts = self.get_hosts()
        for h in hosts:
            host = self.get_hosts(h.id)
            volumes = self._get_sub_resource_by(types.DS8K_HOST, host,
                                                types.DS8K_VOLUME
                                                )
            mappings = self._get_sub_resource_by(types.DS8K_HOST, host,
                                                 types.DS8K_VOLMAP
                                                 )
            ioports = self._get_sub_resource_by(types.DS8K_HOST, host,
                                                types.DS8K_IOPORT
                                                )
            host_ports = self._get_sub_resource_by(types.DS8K_HOST, host,
                                                   types.DS8K_HOST_PORT
                                                   )
            if volumes and mappings and ioports and host_ports:
                return

    def test_host_ports(self):
        ports = self.get_host_ports()
        if ports:
            self.get_host_ports(ports[0].id)

    def _get_volumes_by(self, route, parent_res):
        return self._get_sub_resource_by(route, parent_res, types.DS8K_VOLUME)

    @res_timer_recorder
    def _get_sub_resource_by(self, route, parent_res, sub_route):
        logger.info('Starting GET /{}/{}/{} request'.format(route,
                                                            parent_res.id,
                                                            sub_route
                                                            )
                    )
        # Lazy-loading
        sub_res = getattr(parent_res, sub_route)
        logger.info('Successfully got {} {}'.format(len(sub_res), sub_route))
        logger.info('Finish GET /{}/{}/{} request'.format(route,
                                                          parent_res.id,
                                                          sub_route
                                                          )
                    )
        return sub_res


class TestSCClient(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.client = SCClient(ds8k_device.ipaddr,
                              ds8k_device.username, ds8k_device.password,
                              # hostname='mtc032h.tuc.stglabs.ibm.com',
                              port=ds8k_device.port,
                              )

    def test_volume_create_and_delete(self):
        volume = self._prepare_volume()
        self._destroy_volume(volume.id)

    def test_volume_rename(self):
        new_name = 'test_rename'
        with self.get_test_volume() as volume:
            res = self.client.rename_volume(volume.id, new_name)
            new_volume = self.client.get_volume(volume.id)[0]
            self.assertEqual(new_volume.get('name'), new_name)
            logger.info(
                'Successfully renamed the volume {}, response is {}'.format(
                    volume.id, res
                    )
                )

    def test_volume_extend(self):
        new_size = '7'
        with self.get_test_volume() as volume:
            res = self.client.extend_volume(volume.id, new_size)
            new_volume = self.client.get_volume(volume.id)[0]
            self.assertEqual(new_volume.get('cap'),
                             str(convert_size_gib_to_bytes(int(new_size)))
                             )
            logger.info(
                'Successfully extended the volume {}, response is {}'.format(
                    volume.id, res
                    )
            )

    def test_volume_move(self):
        with self.get_test_volume() as volume:
            pools = self.client.list_extentpools()
            old_pool_id = volume.pool
            for pool in pools:
                if pool.get('id') != old_pool_id:
                    new_pool_id = pool.get('id')
                    res = self.client.relocate_volume(volume.id, new_pool_id)
                    new_volume = self.client.get_volume(volume.id)[0]
                    self.assertEqual(new_volume.get('pool'),
                                     new_pool_id
                                     )
                    logger.info(
                        'Successfully move volume {} from pool {} to pool {}, response is {}'.format(  # noqa
                            volume.id, old_pool_id, new_pool_id, res
                            )
                        )
                    break

    def test_host_create_and_delete(self):
        host_name = self._prepare_host()
        self._destroy_host(host_name)

    def test_volume_map_and_unmap(self):
        with self.get_test_host() as host_name:
            with self.get_test_volume() as volume:
                used_lunids = self.client.get_used_lun_numbers_by_host(
                    host_name
                )
                unused_lunids = \
                    ['{0:0{1}x}'.format(i, 2) for i in range(256)
                     if '{0:0{1}x}'.format(i, 2) not in used_lunids
                     ]
                lunid = unused_lunids[0]
                logger.info(
                    'Trying to map volume {} to host {} with lunid {}'.format(
                        volume.id, host_name, lunid
                    )
                )
                res = self.client.map_volume_to_host(host_name=host_name,
                                                     volume_id=volume.id,
                                                     lunid=lunid
                                                     )
                logger.info(
                    'Successfully map volume {} to host {}. res is {}'.format(
                        volume.id, host_name, res
                    )
                )
                logger.info(
                    'Trying to unmap volume {} from host {}.'.format(
                        volume.id, host_name
                    )
                )
                res = self.client.unmap_volume_from_host(host_name, lunid)
                logger.info(
                    'Successfully unmap volume {} from host {}. res is {}'.format(  # noqa
                        volume.id, host_name, res
                    )
                )

    def test_volume_map_and_unmap_to_zlinux_type_host(self):
        with self.get_test_zlinux_type_host() as host_name:
            with self.get_test_volume() as volume:
                logger.info(
                    'Trying to map volume {} to host {}'.format(
                        volume.id, host_name
                    )
                )
                res = self.client.map_volume_to_host(host_name=host_name,
                                                     volume_id=volume.id,
                                                     lunid=''
                                                     )
                logger.info(
                    'Successfully map volume {} to host {}. res is {}'.format(
                        volume.id, host_name, res
                    )
                )
                logger.info(
                    'Trying to unmap volume {} from host {}.'.format(
                        volume.id, host_name
                    )
                )
                lunid = int('40' + volume.id[:2] + '40' + volume.id[2:], 16)
                res = self.client.unmap_volume_from_host(host_name, lunid)
                logger.info(
                    'Successfully unmap volume {} from host {}. res is {}'.format(  # noqa
                        volume.id, host_name, res
                    )
                )

    def _prepare_volume(self):
        logger.info('Preparing a new volume for test purpose.')
        pools = self.client.list_extentpools()
        res = self.client.create_volumes(pool_id=pools[0].get('id'),
                                         capacity_in_GiB=2,
                                         sam='ese',
                                         volume_names_list=['loutest_volume1']
                                         )
        logger.info('Task done, the volume {} is created.'.format(res))
        return res[0]

    def _destroy_volume(self, volume_id):
        logger.info('Destroying the created volume {}'.format(volume_id))
        # delete may fail if it is mapped to hosts.
        self.client.delete_volume(volume_id)
        logger.info('Task done, the volume is deleted successfully.')

    def _prepare_host(self):
        logger.info('Preparing a new host for test purpose.')
        res = self.client.crate_host(host_name='loutest_host1',
                                     wwpn='1'
                                     )
        logger.info('Task done, the host {} is created.'.format(res))
        return res

    def _prepare_host_of_zlinux(self):
        logger.info('Preparing a new zLinux type host for test purpose.')
        res = self.client.crate_host(host_name='zlinuxtest_host1',
                                     wwpn='1',
                                     host_type='zLinux'
                                     )
        logger.info('Task done, the zLinux type host {} is '
                    'created.'.format(res))
        return res

    def _destroy_host(self, host_name):
        logger.info('Destroying the created host {}'.format(host_name))
        self.client.delete_host(host_name)
        logger.info('Task done, the host is deleted successfully.')

    @contextmanager
    def get_test_volume(self):
        volume = self._prepare_volume()
        try:
            yield volume
        except Exception:
            raise
        finally:
            self._destroy_volume(volume.id)

    @contextmanager
    def get_test_host(self):
        host_name = self._prepare_host()
        try:
            yield host_name
        except Exception:
            raise
        finally:
            self._destroy_host(host_name)

    @contextmanager
    def get_test_zlinux_type_host(self):
        host_name = self._prepare_host_of_zlinux()
        try:
            yield host_name
        except Exception:
            raise
        finally:
            self._destroy_host(host_name)
