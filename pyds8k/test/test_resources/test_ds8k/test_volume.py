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

import httpretty
import json
from nose.tools import nottest
from pyds8k.messages import INVALID_TYPE
from pyds8k.resources.ds8k.v1.common import types
from pyds8k.dataParser.ds8k import RequestParser
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.volumes import Volume, \
    VolumeManager
from pyds8k.resources.ds8k.v1.pools import Pool
from pyds8k.resources.ds8k.v1.hosts import Host
from pyds8k.resources.ds8k.v1.flashcopy import FlashCopy
from pyds8k.resources.ds8k.v1.pprc import PPRC
from pyds8k.resources.ds8k.v1.lss import LSS
from pyds8k.resources.ds8k.v1.common.types import DS8K_VOLUME
from ...data import get_response_json_by_type, get_response_data_by_type
from ...data import action_response_json, action_response, \
    create_volumes_response_json, create_volume_response_json, \
    create_volumes_partial_failed_response_json, \
    create_volumes_partial_failed_response
from pyds8k.exceptions import FieldReadOnly


class TestVolume(TestDS8KWithConnect):

    def setUp(self):
        super(TestVolume, self).setUp()
        self.volume = Volume(self.client, VolumeManager(self.client))
        self.maxDiff = None

    def test_invalid_volume_type(self):
        with self.assertRaises(ValueError) as cm:
            Volume(self.client, volume_type='fake')
        self.assertEqual(
            INVALID_TYPE.format(', '.join(types.DS8K_VOLUME_TYPES)),
            str(cm.exception)
        )

    def test_related_resource_field(self):
        volume_info = get_response_data_by_type(
            DS8K_VOLUME
        )['data'][DS8K_VOLUME][0]
        pool_id = volume_info['pool'][Pool.id_field]
        lss_id = volume_info['lss']['id']
        volume = Volume(self.client, info=volume_info)
        self.assertEqual(volume.pool, pool_id)
        self.assertEqual(volume.representation['pool'], pool_id)
        self.assertIsInstance(volume._pool, Pool)
        self.assertEqual(volume._pool.id, pool_id)
        self.assertEqual(volume.lss, lss_id)
        self.assertEqual(volume.representation['lss'], lss_id)
        self.assertIsInstance(volume._lss, LSS)
        self.assertEqual(volume._lss.id, lss_id)

        volume.pool = 'new_pool'
        self.assertEqual(volume.pool, 'new_pool')
        self.assertEqual(volume.representation['pool'], 'new_pool')

        with self.assertRaises(FieldReadOnly):
            volume.lss = 'new_lss'

    def test_related_resources_collection(self):
        hosts = [Host(self.client, resource_id='host{}'.format(i))
                 for i in range(10)
                 ]

        flashcopies = [FlashCopy(self.client, resource_id='fc{}'.format(i))
                       for i in range(10)
                       ]

        pprc = [PPRC(self.client, resource_id='pprc{}'.format(i))
                for i in range(10)
                ]

        # init without related_resources collection
        volume = Volume(self.client, info={
            'name': 'a_0000',
            'link': {
                'rel': 'self',
                'href': '/api/volumes/a_0000'
            },
            'hosts': {
                'link': {
                    'rel': 'self',
                    'href': '/api/hosts'
                },
            }
        }
                        )
        for i in volume.related_resources_collection:
            self.assertEqual('', volume.representation.get(i))
            self.assertFalse(hasattr(volume, i))

        # loading related resources collection
        volume._start_updating()
        setattr(volume, types.DS8K_HOST, hosts)
        setattr(volume, types.DS8K_FLASHCOPY, flashcopies)
        setattr(volume, types.DS8K_PPRC, pprc)
        volume._stop_updating()
        for j, value in enumerate(volume.representation[types.DS8K_HOST]):
            self.assertEqual(value,
                             getattr(hosts[j], hosts[j].id_field)
                             )
        for k, value in enumerate(volume.representation[types.DS8K_FLASHCOPY]):
            self.assertEqual(value,
                             getattr(flashcopies[k], flashcopies[k].id_field)
                             )
        for l, value in enumerate(volume.representation[types.DS8K_PPRC]):
            self.assertEqual(value,
                             getattr(pprc[l], pprc[l].id_field)
                             )

    @httpretty.activate
    def test_delete_volume(self):
        response_a_json = get_response_json_by_type(DS8K_VOLUME)
        response_a = get_response_data_by_type(DS8K_VOLUME)
        name = self._get_resource_id_from_resopnse(DS8K_VOLUME, response_a,
                                                   Volume.id_field
                                                   )
        url = '/volumes/{}'.format(name)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=response_a_json,
                               content_type='application/json',
                               status=200,
                               )
        httpretty.register_uri(httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_json,
                               content_type='application/json',
                               status=204,
                               )
        # Way 1
        _ = self.system.delete_volume(name)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        volume = self.system.get_volume(name)
        self.assertIsInstance(volume, Volume)
        resp2, _ = volume.delete()
        self.assertEqual(resp2.status_code, 204)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_update_volume_rename(self):
        volume_id = 'a_0000'
        url = '/volumes/{}'.format(volume_id)
        new_name = 'new_name'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'name': new_name})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        res = self.system.update_volume_rename(volume_id, new_name)
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(res, action_response['server'])

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.name = new_name
        _, body = vol.save()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(body, action_response['server'])

    @httpretty.activate
    def test_update_volume_extend(self):
        volume_id = 'a_0000'
        url = '/volumes/{}'.format(volume_id)
        new_size = '100'
        captype = 'gib'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'cap': new_size, 'captype': captype})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        res = self.system.update_volume_extend(volume_id, new_size, captype)
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(res, action_response['server'])

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.cap = new_size
        vol.captype = captype
        _, body = vol.save()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(body, action_response['server'])

    @httpretty.activate
    def test_update_volume_move(self):
        volume_id = 'a_0000'
        url = '/volumes/{}'.format(volume_id)
        new_pool = 'new_pool'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'pool': new_pool})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        res = self.system.update_volume_move(volume_id, new_pool)
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(res, action_response['server'])

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.pool = new_pool
        _, body = vol.save()
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(body, action_response['server'])

    @nottest
    @httpretty.activate
    def test_update_volume_map(self):
        volume_id = 'a_0000'
        url = '/volumes/{}'.format(volume_id)
        host_name = 'host1'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'host': host_name})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        res = self.system.update_volume_map(volume_id, host_name)
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(res, action_response['server'])

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.host = host_name

    @httpretty.activate
    def test_create_volume(self):
        url = '/volumes'

        name = 'volume1'
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            req = RequestParser({'name': name, 'cap': cap,
                                 'pool': pool, 'stgtype': stgtype,
                                 'captype': captype, 'lss': lss, 'tp': tp,
                                 }
                                )
            self.assertDictContainsSubset(
                req.get_request_data().get('request').get('params'),
                json.loads(request.body).get('request').get('params'),
            )
            return (201, headers, create_volume_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        # Way 1
        resp1 = self.system.create_volume(name=name, cap=cap,
                                          pool=pool, stgtype=stgtype,
                                          captype=captype, lss=lss, tp=tp, )
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(resp1[0], Volume)

        # Way 2
        volume = self.system.all(DS8K_VOLUME, rebuild_url=True)
        new_vol2 = volume.create(name=name, cap=cap,
                                 pool=pool, stgtype=stgtype,
                                 captype=captype, lss=lss, tp=tp, )
        resp2, data2 = new_vol2.posta()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data2[0], Volume)
        self.assertEqual(resp2.status_code, 201)

        # Way 3
        volume = self.system.all(DS8K_VOLUME, rebuild_url=True)
        new_vol3 = volume.create(name=name, cap=cap,
                                 pool=pool, stgtype=stgtype,
                                 captype=captype, lss=lss, tp=tp, )
        resp3, data3 = new_vol3.save()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data3[0], Volume)
        self.assertEqual(resp3.status_code, 201)

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.

    @httpretty.activate
    def test_create_volumes(self):
        url = '/volumes'

        name = 'volume1'
        quantity = '10'
        namecol = ['volume{}'.format(i) for i in range(10)]
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'

        def _verify_request1(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'name': name, 'cap': cap,
                                  'pool': pool, 'stgtype': stgtype,
                                  'captype': captype, 'lss': lss, 'tp': tp,
                                  'quantity': quantity, 'namecol': '',
                                  })
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (201, headers, create_volumes_response_json)

        def _verify_request2(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'namecol': namecol, 'cap': cap,
                                  'pool': pool, 'stgtype': stgtype,
                                  'name': '', 'quantity': '',
                                  'captype': captype, 'lss': lss, 'tp': tp,
                                  })
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (201, headers, create_volumes_response_json)

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            responses=[
                httpretty.Response(body=_verify_request1,
                                   content_type='application/json',
                                   ),
                httpretty.Response(body=_verify_request2,
                                   content_type='application/json',
                                   ),
            ]
        )

        resp1 = self.system.create_volumes_with_same_prefix(
            name=name,
            cap=cap,
            pool=pool, stgtype=stgtype,
            captype=captype, lss=lss,
            tp=tp, quantity=quantity,
        )
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(resp1[0], Volume)

        resp2 = self.system.create_volumes_without_same_prefix(
            name_col=namecol,
            cap=cap,
            pool=pool, stgtype=stgtype,
            captype=captype, lss=lss,
            tp=tp,
        )
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(resp2[0], Volume)

    @httpretty.activate
    def test_create_volumes_partial_failed(self):
        url = '/volumes'

        name = 'volume1'
        quantity = '10'
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'

        def _verify_request1(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'name': name, 'cap': cap,
                                  'pool': pool, 'stgtype': stgtype,
                                  'captype': captype, 'lss': lss, 'tp': tp,
                                  'quantity': quantity, 'namecol': '',
                                  })
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (201, headers, create_volumes_partial_failed_response_json)

        httpretty.register_uri(
            httpretty.POST,
            self.domain + self.base_url + url,
            responses=[
                httpretty.Response(body=_verify_request1,
                                   content_type='application/json',
                                   ),
            ]
        )

        resp1 = self.system.create_volumes_with_same_prefix(
            name=name,
            cap=cap,
            pool=pool, stgtype=stgtype,
            captype=captype, lss=lss,
            tp=tp, quantity=quantity,
        )
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        # return 1 created volume and 1 error status
        self.assertIsInstance(resp1[0], Volume)
        self.assertIsInstance(resp1[1], dict)
        self.assertEqual(
            resp1[1],
            create_volumes_partial_failed_response.get('responses'
                                                       )[1].get('server')
        )

    def test_create_volume_type_error(self):
        with self.assertRaises(ValueError):
            self.system.create_volume('name', '10', 'testpool_0',
                                      'fake_stgtype'
                                      )
        with self.assertRaises(ValueError):
            self.system.create_volume('name', '10', 'testpool_0',
                                      types.DS8K_VOLUME_TYPE_FB,
                                      captype='fake_captype')
        with self.assertRaises(ValueError):
            self.system.create_volume('name', '10', 'testpool_0',
                                      types.DS8K_VOLUME_TYPE_FB,
                                      tp='fake_tp')
