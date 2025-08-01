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
import json
from functools import cmp_to_key
from http import HTTPStatus

import pytest
import responses
from responses import matchers

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.messages import INVALID_TYPE
from pyds8k.resources.ds8k.v1.common import types
from pyds8k.resources.ds8k.v1.common.types import DS8K_LSS, DS8K_VOLUME
from pyds8k.resources.ds8k.v1.lss import LSS, LSSManager
from pyds8k.resources.ds8k.v1.volumes import Volume
from pyds8k.test.data import (
    create_lss_response,
    get_response_json_by_type,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect


class TestLSS(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.lss = LSS(self.client, LSSManager(self.client))

    def test_get_volumes(self):
        self._test_sub_resource_list_by_route(
            DS8K_LSS, DS8K_VOLUME, self._sorted_by_volume_name
        )

    def test_set_related_resources_collection(self):
        volumes = [Volume(self.client, resource_id=f'volume{i}') for i in range(10)]

        # init without related_resources collection
        lss = LSS(
            self.client,
            info={
                'volumes': {
                    'link': {'rel': 'self', 'href': '/api/volumes'},
                }
            },
        )
        for i in lss.related_resources_collection:
            assert lss.representation.get(i) == ''
            assert not hasattr(lss, i)

        # loading related resources collection
        lss._start_updating()
        for item in ((DS8K_VOLUME, volumes),):
            setattr(lss, item[0], item[1])
            for j, value in enumerate(lss.representation[item[0]]):
                assert value == getattr(item[1][j], item[1][j].id_field)
        lss._stop_updating()

    @responses.activate
    def test_lazy_loading_related_resources_collection(self):
        lss_id = '00'
        url = f'/lss/{lss_id}'
        responses.get(
            self.domain + self.base_url + url,
            body=get_response_json_by_type(DS8K_LSS),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        for item in LSS.related_resources_collection:
            sub_route_url = f'{url}/{item}'
            responses.get(
                self.domain + self.base_url + sub_route_url,
                body=get_response_list_json_by_type(item),
                content_type='application/json',
                status=HTTPStatus.OK.value,
            )
        lss = self.system.get_lss_by_id(lss_id)

        for item in LSS.related_resources_collection:
            res_collection = getattr(lss, item)
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
        lss = LSS(
            self.client,
            info={
                'volumes': [
                    {
                        'id': '0000',
                        'link': {'rel': 'self', 'href': '/api/volumes/0000'},
                    },
                ],
            },
        )

        assert lss.representation.get('volumes')[0] == '0000'
        assert lss.volumes[0].id == '0000'

    def test_invalid_lss_type(self):
        with pytest.raises(
            ValueError, match=INVALID_TYPE.format(', '.join(types.DS8K_LSS_TYPES))
        ):
            LSS(self.client, lss_type="fake")

    def test_invalid_ckd_based_cu_type(self):
        with pytest.raises(
            ValueError, match=INVALID_TYPE.format(', '.join(types.DS8K_LCU_TYPES))
        ):
            LSS(self.client, lcu_type="fake")

    @responses.activate
    def test_create_lss_ckd(self):
        url = '/lss'
        uri = f'{self.domain}{self.base_url}{url}'

        struct_request = {
            'id': 'FE',
            'type': 'ckd',
            'sub_system_identifier': 'FE00',
            'ckd_base_cu_type': types.DS8K_LCU_TYPE_3990_6,
        }

        req = RequestParser(struct_request)
        responses.post(
            uri,
            status=HTTPStatus.OK,
            body=json.dumps(create_lss_response),
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        resp = self.system.create_lss_ckd(
            lss_id=struct_request['id'],
            lss_type=struct_request['type'],
            lcu_type=struct_request['ckd_base_cu_type'],
            ss_id=struct_request['sub_system_identifier'],
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp[0], LSS)
