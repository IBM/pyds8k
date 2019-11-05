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
from functools import cmp_to_key
from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_POOL, \
    DS8K_VOLUME, \
    DS8K_TSEREP, \
    DS8K_ESEREP
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type, \
    get_response_json_by_type, \
    get_response_data_by_type
from ...data import action_response, action_response_json
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.resources.ds8k.v1.pools import Pool
from pyds8k.resources.ds8k.v1.tserep import TSERep
from pyds8k.resources.ds8k.v1.eserep import ESERep

response_a = get_response_data_by_type(DS8K_POOL)
response_a_json = get_response_json_by_type(DS8K_POOL)


class TestPool(TestDS8KWithConnect):

    def setUp(self):
        super(TestPool, self).setUp()
        self.pool_id = self._get_resource_id_from_resopnse(DS8K_POOL,
                                                           response_a,
                                                           Pool.id_field
                                                           )
        self.pool = self.system.one(
            DS8K_POOL,
            self.pool_id,
            rebuild_url=True
        )

    def test_get_volumes(self):
        self._test_sub_resource_list_by_route(DS8K_POOL, DS8K_VOLUME,
                                              self._sorted_by_volume_name
                                              )

    def test_get_tserep(self):
        self._test_sub_resource_list_by_route(DS8K_POOL, DS8K_TSEREP)

    def test_get_eserep(self):
        self._test_sub_resource_list_by_route(DS8K_POOL, DS8K_ESEREP)

    @httpretty.activate
    def test_delete_tserep(self):
        url = '/pools/{}/tserep'.format(self.pool_id)
        httpretty.register_uri(
            httpretty.DELETE,
            self.domain + self.base_url + url,
            content_type='application/json',
            status=204,
        )
        self.pool.delete_tserep()
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_delete_eserep(self):
        url = '/pools/{}/eserep'.format(self.pool_id)
        httpretty.register_uri(
            httpretty.DELETE,
            self.domain + self.base_url + url,
            content_type='application/json',
            status=204,
        )
        self.pool.delete_eserep()
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

    @httpretty.activate
    def test_update_tserep_cap(self):
        url = '/pools/{}/tserep'.format(self.pool_id)
        cap = '10'
        captype = 'gib'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'cap': cap, 'captype': captype})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        _, body = self.pool.update_tserep_cap(cap, captype)
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(body, action_response['server'])

    @httpretty.activate
    def test_update_tserep_threshold(self):
        url = '/pools/{}/tserep'.format(self.pool_id)
        threshold = '70'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            resq = RequestParser({'threshold': threshold})
            self.assertEqual(json.loads(request.body), resq.get_request_data())
            return (200, headers, action_response_json)

        httpretty.register_uri(httpretty.PUT,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        _, body = self.pool.update_tserep_threshold(threshold)
        self.assertEqual(httpretty.PUT, httpretty.last_request().method)
        self.assertEqual(body, action_response['server'])

    def test_update_eserep_cap(self):
        pass

    def test_update_eserep_threshold(self):
        pass

    def test_set_related_resources_collection(self):
        volumes = [Volume(self.client, resource_id='volume{}'.format(i))
                   for i in range(10)
                   ]
        tserep = [TSERep(self.client, info={'pool': {'name': 'testpool_0'}}), ]
        eserep = [ESERep(self.client, info={'pool': {'name': 'testpool_0'}}), ]

        # init without related_resources collection
        pool = Pool(self.client, info={
            'name': 'testpool_0',
            'eserep': '',
            'tserep': '',
            'volumes': {
                'link': {
                    'rel': 'self',
                    'href': '/api/volumes'
                },
            }
        }
                    )
        for i in pool.related_resources_collection:
            self.assertEqual('', pool.representation.get(i))
            self.assertFalse(hasattr(pool, i))

        # loading related resources collection
        pool._start_updating()
        for item in ((DS8K_VOLUME, volumes),
                     (DS8K_TSEREP, tserep),
                     (DS8K_ESEREP, eserep),
                     ):
            setattr(pool, item[0], item[1])
            for j, value in enumerate(pool.representation[item[0]]):
                self.assertEqual(value,
                                 getattr(item[1][j], item[1][j].id_field)
                                 )
        pool._stop_updating()

    @httpretty.activate
    def test_lazy_loading_related_resources_collection(self):
        url = '/pools/{}'.format(self.pool_id)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=response_a_json,
                               content_type='application/json',
                               status=200,
                               )
        for item in Pool.related_resources_collection:
            sub_route_url = '{}/{}'.format(url, item)
            httpretty.register_uri(httpretty.GET,
                                   self.domain + self.base_url + sub_route_url,
                                   body=get_response_list_json_by_type(item),
                                   content_type='application/json',
                                   status=200,
                                   )
        pool = self.system.get_pool(self.pool_id)

        for item in Pool.related_resources_collection:
            res_collection = getattr(pool, item)
            self.assertNotEqual(0, len(res_collection))
            res_collection.sort(
                key=cmp_to_key(
                    self._get_sort_func_by(res_collection[0].id_field))
            )
            res_collection_data = list(
                get_response_list_data_by_type(item)['data'][item]
            )
            res_collection_data.sort(
                key=cmp_to_key(
                    self._get_sort_func_by(res_collection[0].id_field))
            )

            self.assertEqual(
                len(res_collection_data),
                len(res_collection))
            self._assert_equal_between_sorted_dict_and_resource_list(
                res_collection_data,
                res_collection
            )

    def test_set_related_resources_collection_during_loading(self):
        pool = Pool(self.client, info={
            'name': 'testpool_0',
            'volumes': [{
                'id': '0000',
                'link': {
                    'rel': 'self',
                    'href': '/api/volumes/0000'
                },
            },
            ],
        }
                    )

        self.assertEqual('0000', pool.representation.get('volumes')[0])
        self.assertEqual('0000', pool.volumes[0].id)
