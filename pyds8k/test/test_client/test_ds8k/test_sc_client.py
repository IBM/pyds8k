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

from pyds8k.resources.ds8k.v1.common import types
from ...base import TestCaseWithConnect
from ...test_resources.test_ds8k.base import TestUtils
from pyds8k.resources.ds8k.v1.common.base import Base
from pyds8k.dataParser.ds8k import ResponseParser, RequestParser
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type, \
    get_response_json_by_type, \
    get_response_data_by_type, \
    get_request_json_body, create_mappings_response_json
from pyds8k.client.ds8k.v1.sc_client import SCClient
import httpretty
from pyds8k.resources.utils import get_resource_class_by_name
from pyds8k.base import Resource

system_list_res_json = get_response_list_json_by_type(types.DS8K_SYSTEM)
system_list_res = get_response_list_data_by_type(types.DS8K_SYSTEM)
volume_list_res_json = get_response_list_json_by_type(types.DS8K_VOLUME)
volume_list_res = get_response_list_data_by_type(types.DS8K_VOLUME)
volume_a_res_json = get_response_json_by_type(types.DS8K_VOLUME)
volume_a_res = get_response_data_by_type(types.DS8K_VOLUME)


class TestClient(TestUtils, TestCaseWithConnect):

    def setUp(self):
        super(TestClient, self).setUp()
        self.base_url = Base.base_url
        self.rest_client = SCClient('localhost', 'admin', 'admin', '8088')

    def _assert_equal_between_dicts(self,
                                    returned_dict,
                                    origin_dict
                                    ):
        for key, value in origin_dict.items():
            if not isinstance(value, dict):
                self.assertEqual(value, returned_dict.get(key))

    def _assert_equal_between_obj_and_dict(self,
                                           returned_obj,
                                           origin_dict
                                           ):
        for key, value in origin_dict.items():
            if not isinstance(value, dict):
                self.assertEqual(value, getattr(returned_obj, key))

    def _set_resource_list(self, route):
        resource_response = get_response_data_by_type(route)
        prefix = '{}.{}'.format(self.client.service_type,
                                self.client.service_version
                                )
        res_class, _ = get_resource_class_by_name(str(route).lower(),
                                                  prefix
                                                  )
        if res_class.__name__ == Resource.__name__:
            raise Exception(
                'Can not get resource class from route: {}'.format(route)
                )
        id_field = res_class.id_field
        route_id = self._get_resource_id_from_resopnse(route,
                                                       resource_response,
                                                       id_field
                                                       )
        url = '/{}/{}'.format(route, route_id)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=get_response_json_by_type(route),
                               content_type='application/json',
                               status=200,
                               )
        return route_id

    def _set_sub_resource(self, route, route_id, sub_route):
        sub_route_url = '/{}/{}/{}'.format(route, route_id, sub_route)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + sub_route_url,
                               body=get_response_list_json_by_type(sub_route),
                               content_type='application/json',
                               status=200,
                               )

    def _post_sub_resource(self, route, route_id, sub_route, body):
        sub_route_url = '/{}/{}/{}'.format(route, route_id, sub_route)

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + sub_route_url)

            resq = RequestParser(body)
            self.assertEqual(get_request_json_body(request.body),
                             resq.get_request_data())
            return (200, headers, create_mappings_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + sub_route_url,
                               body=_verify_request,
                               content_type='application/json',
                               )

    @httpretty.activate
    def _test_resource_by_route(self, route, func, sub_resource=[]):
        route_id = self._set_resource_list(route)
        if sub_resource:
            for sub_route in sub_resource:
                self._set_sub_resource(route, route_id, sub_route)
        res = getattr(self.rest_client, func)(route_id)[0]
        self.assertIsInstance(res, dict)
        rep = ResponseParser(get_response_data_by_type(route),
                             route).get_representations()[0]
        self._assert_equal_between_dicts(res, rep)

    @httpretty.activate
    def _test_sub_resource(self, route, sub_route, func):
        route_id = self._set_resource_list(route)
        self._set_sub_resource(route, route_id, sub_route)
        res = getattr(self.rest_client, func)(route_id)[0]
        self.assertIsInstance(res, dict)
        # print "&&&&&&&&&&&{}".format(res)
        rep = ResponseParser(get_response_data_by_type(sub_route),
                             sub_route).get_representations()[0]
        self._assert_equal_between_dicts(res, rep)

    @httpretty.activate
    def _test_resource_list_by_route(self, route, func=None):
        prefix = '{}.{}'.format(self.client.service_type,
                                self.client.service_version
                                )
        res_class, _ = get_resource_class_by_name(str(route).lower(),
                                                  prefix
                                                  )
        if res_class.__name__ == Resource.__name__:
            raise Exception(
                'Can not get resource class from route: {}'.format(route)
                )
        url = '/{}'.format(route)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=get_response_list_json_by_type(route),
                               content_type='application/json',
                               status=200,
                               )
        func = func or 'get_{}'.format(route)
        res = getattr(self.rest_client, func)()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)
        # print "&&&&&&&&&&&{}".format(res[0])
        rep = ResponseParser(get_response_list_data_by_type(route),
                             route).get_representations()[0]
        self._assert_equal_between_dicts(res[0], rep)

    @httpretty.activate
    def _test_sub_resource_post(self, route, sub_route, func, body, *params):
        route_id = self._set_resource_list(route)
        self._post_sub_resource(route, route_id, sub_route, body)
        func = func or 'get_{}'.format(route)
        res = getattr(self.rest_client, func)(route_id, *params)[0]
        rep = ResponseParser(get_response_data_by_type(sub_route),
                             sub_route).get_representations()[0]
        self._assert_equal_between_obj_and_dict(res, rep)

    @httpretty.activate
    def test_get_system(self):
        sys_url = '/systems'

        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + sys_url,
                               body=system_list_res_json,
                               content_type='application/json')

        sys = self.rest_client.get_system()[0]
        self.assertIsInstance(sys, dict)
        rep = ResponseParser(system_list_res,
                             types.DS8K_SYSTEM).get_representations()[0]
        self._assert_equal_between_dicts(sys, rep)

    def test_get_volume(self):
        self._test_resource_by_route(types.DS8K_VOLUME, 'get_volume')

    def test_get_extentpool(self):
        self._test_resource_by_route(types.DS8K_POOL, 'get_extentpool',
                                     sub_resource=[types.DS8K_ESEREP, ])

    def test_list_extentpools(self):
        self._test_resource_list_by_route(types.DS8K_POOL, 'list_extentpools')

    def test_list_extentpool_volumes(self):
        self._test_sub_resource(types.DS8K_POOL,
                                types.DS8K_VOLUME,
                                'list_extentpool_volumes',
                                )

    def test_list_extentpool_virtualpool(self):
        self._test_sub_resource(types.DS8K_POOL,
                                types.DS8K_ESEREP,
                                'list_extentpool_virtualpool',
                                )

    def test_list_flashcopies(self):
        self._test_resource_list_by_route(types.DS8K_FLASHCOPY,
                                          'list_flashcopies'
                                          )

    def test_list_volume_flashcopies(self):
        self._test_sub_resource(types.DS8K_VOLUME,
                                types.DS8K_FLASHCOPY,
                                'list_volume_flashcopies',
                                )

    def test_list_remotecopies(self):
        self._test_resource_list_by_route(types.DS8K_PPRC,
                                          'list_remotecopies'
                                          )

    def test_list_volume_remotecopies(self):
        self._test_sub_resource(types.DS8K_VOLUME,
                                types.DS8K_PPRC,
                                'list_volume_remotecopies',
                                )

    def test_list_logical_subsystems(self):
        self._test_resource_list_by_route(types.DS8K_LSS,
                                          'list_logical_subsystems'
                                          )

    def test_list_lss_volumes(self):
        self._test_sub_resource(types.DS8K_LSS,
                                types.DS8K_VOLUME,
                                'list_lss_volumes',
                                )

    def test_list_fcports(self):
        self._test_resource_list_by_route(types.DS8K_IOPORT,
                                          'list_fcports'
                                          )

    def test_map_volume_to_host(self):
        volume_id = '000B'
        lunid = '09'
        body = {"mappings": [{lunid: volume_id}, ]}
        self._test_sub_resource_post(types.DS8K_HOST,
                                     types.DS8K_VOLMAP,
                                     'map_volume_to_host',
                                     body,
                                     volume_id,
                                     lunid
                                     )
        body = {"volumes": [volume_id]}
        self._test_sub_resource_post(types.DS8K_HOST,
                                     types.DS8K_VOLMAP,
                                     'map_volume_to_host',
                                     body,
                                     volume_id,
                                     ''
                                     )
