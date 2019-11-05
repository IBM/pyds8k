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
from functools import cmp_to_key
from pyds8k.resources.ds8k.v1.common.types import DS8K_LSS, \
    DS8K_VOLUME
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type, \
    get_response_json_by_type
from .base import TestDS8KWithConnect
from pyds8k.resources.ds8k.v1.lss import LSS, LSSManager
from pyds8k.resources.ds8k.v1.volumes import Volume


class TestLSS(TestDS8KWithConnect):

    def setUp(self):
        super(TestLSS, self).setUp()
        self.lss = LSS(self.client, LSSManager(self.client))

    def test_get_volumes(self):
        self._test_sub_resource_list_by_route(DS8K_LSS, DS8K_VOLUME,
                                              self._sorted_by_volume_name
                                              )

    def test_set_related_resources_collection(self):
        volumes = [Volume(self.client, resource_id='volume{}'.format(i))
                   for i in range(10)
                   ]

        # init without related_resources collection
        lss = LSS(self.client, info={
            'volumes': {
                'link': {
                    'rel': 'self',
                    'href': '/api/volumes'
                },
            }
        }
                  )
        for i in lss.related_resources_collection:
            self.assertEqual('', lss.representation.get(i))
            self.assertFalse(hasattr(lss, i))

        # loading related resources collection
        lss._start_updating()
        for item in ((DS8K_VOLUME, volumes),
                     ):
            setattr(lss, item[0], item[1])
            for j, value in enumerate(lss.representation[item[0]]):
                self.assertEqual(value,
                                 getattr(item[1][j], item[1][j].id_field)
                                 )
        lss._stop_updating()

    @httpretty.activate
    def test_lazy_loading_related_resources_collection(self):
        lss_id = '00'
        url = '/lss/{}'.format(lss_id)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=get_response_json_by_type(DS8K_LSS),
                               content_type='application/json',
                               status=200,
                               )
        for item in LSS.related_resources_collection:
            sub_route_url = '{}/{}'.format(url, item)
            httpretty.register_uri(httpretty.GET,
                                   self.domain + self.base_url + sub_route_url,
                                   body=get_response_list_json_by_type(item),
                                   content_type='application/json',
                                   status=200,
                                   )
        lss = self.system.get_lss_by_id(lss_id)

        for item in LSS.related_resources_collection:
            res_collection = getattr(lss, item)
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
        lss = LSS(self.client, info={
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

        self.assertEqual('0000', lss.representation.get('volumes')[0])
        self.assertEqual('0000', lss.volumes[0].id)
