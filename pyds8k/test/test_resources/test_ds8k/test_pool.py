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

from functools import cmp_to_key
from http import HTTPStatus

import responses
from responses import matchers

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import (
    DS8K_ESEREP,
    DS8K_POOL,
    DS8K_TSEREP,
    DS8K_VOLUME,
)
from pyds8k.resources.ds8k.v1.eserep import ESERep
from pyds8k.resources.ds8k.v1.pools import Pool
from pyds8k.resources.ds8k.v1.tserep import TSERep
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.test.data import (
    action_response,
    action_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect

response_a = get_response_data_by_type(DS8K_POOL)
response_a_json = get_response_json_by_type(DS8K_POOL)


class TestPool(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.pool_id = self._get_resource_id_from_resopnse(
            DS8K_POOL, response_a, Pool.id_field
        )
        self.pool = self.system.one(DS8K_POOL, self.pool_id, rebuild_url=True)

    def test_get_volumes(self):
        self._test_sub_resource_list_by_route(
            DS8K_POOL, DS8K_VOLUME, self._sorted_by_volume_name
        )

    def test_get_tserep(self):
        self._test_sub_resource_list_by_route(DS8K_POOL, DS8K_TSEREP)

    def test_get_eserep(self):
        self._test_sub_resource_list_by_route(DS8K_POOL, DS8K_ESEREP)

    @responses.activate
    def test_delete_tserep(self):
        url = f'/pools/{self.pool_id}/tserep'
        responses.delete(
            self.domain + self.base_url + url,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        self.pool.delete_tserep()
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_delete_eserep(self):
        url = f'/pools/{self.pool_id}/eserep'
        responses.delete(
            self.domain + self.base_url + url,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        self.pool.delete_eserep()
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_update_tserep_cap(self):
        url = f'/pools/{self.pool_id}/tserep'
        uri = f'{self.domain}{self.base_url}{url}'

        cap = '10'
        captype = 'gib'

        resq = RequestParser({'cap': cap, 'captype': captype})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )
        _, body = self.pool.update_tserep_cap(cap, captype)
        assert responses.calls[-1].request.method == responses.PUT
        assert body == action_response['server']

    @responses.activate
    def test_update_tserep_threshold(self):
        url = f'/pools/{self.pool_id}/tserep'
        uri = f'{self.domain}{self.base_url}{url}'

        threshold = '70'

        resq = RequestParser({'threshold': threshold})
        responses.put(
            uri,
            status=HTTPStatus.CREATED,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )
        _, body = self.pool.update_tserep_threshold(threshold)
        assert responses.calls[-1].request.method == responses.PUT
        assert body == action_response['server']

    def test_update_eserep_cap(self):
        pass

    def test_update_eserep_threshold(self):
        pass

    def test_set_related_resources_collection(self):
        volumes = [Volume(self.client, resource_id=f'volume{i}') for i in range(10)]
        tserep = [
            TSERep(self.client, info={'pool': {'name': 'testpool_0'}}),
        ]
        eserep = [
            ESERep(self.client, info={'pool': {'name': 'testpool_0'}}),
        ]

        # init without related_resources collection
        pool = Pool(
            self.client,
            info={
                'name': 'testpool_0',
                'eserep': '',
                'tserep': '',
                'volumes': {
                    'link': {'rel': 'self', 'href': '/api/volumes'},
                },
            },
        )
        for i in pool.related_resources_collection:
            assert pool.representation.get(i) == ''
            assert not hasattr(pool, i)

        # loading related resources collection
        pool._start_updating()
        for item in (
            (DS8K_VOLUME, volumes),
            (DS8K_TSEREP, tserep),
            (DS8K_ESEREP, eserep),
        ):
            setattr(pool, item[0], item[1])
            for j, value in enumerate(pool.representation[item[0]]):
                assert value == getattr(item[1][j], item[1][j].id_field)
        pool._stop_updating()

    @responses.activate
    def test_lazy_loading_related_resources_collection(self):
        url = f'/pools/{self.pool_id}'
        responses.get(
            self.domain + self.base_url + url,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        for item in Pool.related_resources_collection:
            sub_route_url = f'{url}/{item}'
            responses.get(
                self.domain + self.base_url + sub_route_url,
                body=get_response_list_json_by_type(item),
                content_type='application/json',
                status=HTTPStatus.OK.value,
            )
        pool = self.system.get_pool(self.pool_id)

        for item in Pool.related_resources_collection:
            res_collection = getattr(pool, item)
            assert len(res_collection) != 0
            res_collection.sort(
                key=cmp_to_key(self._get_sort_func_by(res_collection[0].id_field))
            )
            res_collection_data = list(
                get_response_list_data_by_type(item)['data'][item]
            )
            res_collection_data.sort(
                key=cmp_to_key(self._get_sort_func_by(res_collection[0].id_field))
            )

            assert len(res_collection_data) == len(res_collection)
            self._assert_equal_between_sorted_dict_and_resource_list(
                res_collection_data, res_collection
            )

    def test_set_related_resources_collection_during_loading(self):
        pool = Pool(
            self.client,
            info={
                'name': 'testpool_0',
                'volumes': [
                    {
                        'id': '0000',
                        'link': {'rel': 'self', 'href': '/api/volumes/0000'},
                    },
                ],
            },
        )

        assert pool.representation.get('volumes')[0] == '0000'
        assert pool.volumes[0].id == '0000'
