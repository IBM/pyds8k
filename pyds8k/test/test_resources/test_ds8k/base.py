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
import operator
from functools import partial, cmp_to_key
from ...data import get_response_list_json_by_type, \
    get_response_list_data_by_type, \
    get_response_data_by_type, \
    get_response_json_by_type
from ... import base
from pyds8k.base import Resource
from pyds8k.resources.ds8k.v1.common.base import Base
from pyds8k.resources.ds8k.v1.common import types
from pyds8k.resources.ds8k.v1.systems import System, \
    SystemManager
from pyds8k.resources.utils import get_resource_class_by_name


def cmp(a, b):
    if a is not None and b is not None:
        return operator.gt(a, b) - operator.lt(a, b)
    else:
        return 0


class TestUtils(object):

    def _sort_by(self, key, obj1, obj2):
        if isinstance(obj1, dict):
            return cmp(obj1.get(key),
                       obj2.get(key)
                       )
        return cmp(getattr(obj1, key),
                   getattr(obj2, key)
                   )

    def _sorted_by_volume_name(self, obj1, obj2):
        return self._sort_by('name', obj1, obj2)

    def _sorted_by_id(self, obj1, obj2):
        return self._sort_by('id', obj1, obj2)

    def _get_sort_func_by(self, key):
        return partial(self._sort_by, key)

    def _assert_equal_between_dict_and_resource(self,
                                                dicte,
                                                resource
                                                ):
        for key, value in dicte.items():
            if not isinstance(value, (dict, list)) and key not in resource.related_resources_collection:  # noqa
                self.assertEqual(value, getattr(resource, key))
                self.assertEqual(value, resource.representation.get(key))

    def _assert_equal_between_sorted_dict_and_resource_list(self,
                                                            dict_list,
                                                            resource_list
                                                            ):
        for index, re in enumerate(resource_list):
            self._assert_equal_between_dict_and_resource(dict_list[index], re)

    @httpretty.activate
    def _test_resource_by_route(self, route):
        resource_response = get_response_data_by_type(route)
        res_class = self._get_class_by_name(route)
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
        res = getattr(self.system,
                      'get_{}'.format(route)
                      )(route_id)
        self.assertIsInstance(res, res_class)
        res_data = resource_response['data'][route][0]
        self._assert_equal_between_dict_and_resource(res_data, res)

    @httpretty.activate
    def _test_resource_list_by_route(self, route, cmp_func=None):
        res_list_resp = get_response_list_data_by_type(route)
        url = '/{}'.format(route)
        res_class = self._get_class_by_name(route)
        id_field = res_class.id_field
        cmp_f = cmp_func if cmp_func else self._get_sort_func_by(id_field)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=get_response_list_json_by_type(route),
                               content_type='application/json',
                               status=200,
                               )
        res_list = getattr(self.system, 'get_{}'.format(route))()
        self.assertIsInstance(res_list[0], res_class)
        res_list.sort(key=cmp_to_key(cmp_f))
        res_list_data = list(res_list_resp['data'][route])
        res_list_data.sort(key=cmp_to_key(cmp_f))
        self.assertEqual(len(res_list_data),
                         len(res_list)
                         )
        self._assert_equal_between_sorted_dict_and_resource_list(
            res_list_data,
            res_list
        )

    @httpretty.activate
    def _test_sub_resource_list_by_route(self, route, sub_route,
                                         cmp_func=None
                                         ):
        sub_res_list_resp = get_response_list_data_by_type(sub_route)
        res_resp = get_response_data_by_type(route)
        res_class = self._get_class_by_name(route)
        id_field = res_class.id_field
        route_id = self._get_resource_id_from_resopnse(route,
                                                       res_resp,
                                                       id_field
                                                       )
        route_url = '/{}/{}'.format(route, route_id)
        sub_route_url = '/{}/{}/{}'.format(route, route_id, sub_route)
        cmp_f = cmp_func if cmp_func else self._sorted_by_id
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + sub_route_url,
                               body=get_response_list_json_by_type(sub_route),
                               content_type='application/json',
                               status=200,
                               )
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + route_url,
                               body=get_response_json_by_type(route),
                               content_type='application/json',
                               status=200,
                               )
        try:
            res = getattr(
                self.system,
                'get_{}'.format(route)
            )(route_id)
        except AttributeError:
            if route == types.DS8K_LSS:
                res = self.system.get_lss_by_id(route_id)
            else:
                raise Exception(
                    'Failed calling get_{}'.format(route)
                )
        self.assertIsInstance(res, res_class)
        sub_res_list = getattr(res, 'get_{}'.format(sub_route))()
        self.assertIs(getattr(res, sub_route), sub_res_list)
        sub_res_list.sort(key=cmp_to_key(cmp_f))
        sub_res_list_data = list(sub_res_list_resp['data'][sub_route])
        sub_res_list_data.sort(key=cmp_to_key(cmp_f))
        self.assertNotEqual(0, len(sub_res_list))
        self.assertEqual(len(sub_res_list_data),
                         len(sub_res_list)
                         )
        self._assert_equal_between_sorted_dict_and_resource_list(
            sub_res_list_data,
            sub_res_list
        )

    def _test_related_resource_field(self, route):
        info = get_response_data_by_type(
            route
        )['data'][route][0]
        res_class = self._get_class_by_name(route)
        for rel, relclass_tuple in res_class.related_resource.items():
            rel_class, _ = relclass_tuple
            rel_id = info[rel[1:]][rel_class.id_field]
            res = res_class(self.client, info=info)
            self.assertEqual(getattr(res, rel[1:]), rel_id)
            self.assertEqual(res.representation[rel[1:]],
                             rel_id
                             )
            self.assertIsInstance(getattr(res, rel), rel_class)
            self.assertEqual(getattr(res, rel).id, rel_id)

    def _get_resource_id_from_resopnse(self, route, response, id_field='id'):
        try:
            return response.get('data').get(route)[0][id_field]
        except Exception:
            raise Exception(
                'Can not get the id of {} from response.'.format(route)
            )

    def _get_resource_ids_from_resopnse(self, route, response, id_field='id'):
        try:
            return [re[id_field] for re in response.get('data').get(route)]
        except Exception:
            raise Exception(
                'Can not get the id of {} from response.'.format(route)
            )

    def _get_class_by_name(self, name):
        prefix = '{}.{}'.format(self.client.service_type,
                                self.client.service_version
                                )
        res_class, _ = get_resource_class_by_name(str(name).lower(),
                                                  prefix
                                                  )
        if res_class.__name__ == Resource.__name__:
            raise Exception(
                'Can not get resource class from route: {}'.format(name)
            )
        return res_class


class TestDS8KWithConnect(TestUtils, base.TestCaseWithConnect):

    def setUp(self):
        super(TestDS8KWithConnect, self).setUp()
        self.base_url = Base.base_url
        self.system = System(self.client, SystemManager(self.client))
