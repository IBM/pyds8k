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

from pyds8k.base import Resource, DefaultManager
from . import base
import httpretty
import json
from pyds8k.messages import DEFAULT_SUCCESS_BODY_DICT
from .data import get_response_list_json_by_type, \
    get_response_list_data_by_type, \
    get_response_data_by_type, \
    get_response_json_by_type
from .data import action_response, action_response_json
from .data import default_template

info = {'id': 'v1', 'name': 'vol1'}

custom_method_get = {'msg': 'custom_method_get'}
custom_method_get_json = json.dumps(custom_method_get)

DEFAULT = 'default'
default_a_response = get_response_data_by_type(DEFAULT)
default_a_response_json = get_response_json_by_type(DEFAULT)
default_list_response = get_response_list_data_by_type(DEFAULT)
default_list_response_json = get_response_list_json_by_type(DEFAULT)


# Note: The ds8k's data parser will be treated as the default parser here.
class TestResource(base.TestCaseWithConnect):

    def setUp(self):
        super(TestResource, self).setUp()
        self.base_url = ''

    def test_one_all(self):
        url1 = '/default/a/default/b/default'
        url2 = '/default/a/default/b/default/c'
        vol1 = self.resource.one(
                                 DEFAULT,
                                 'a'
                                 ).one(
                                       DEFAULT,
                                       'b'
                                       ).all(DEFAULT)
        vol2 = self.resource.one(
                                 DEFAULT,
                                 'a'
                                 ).one(
                                       DEFAULT,
                                       'b'
                                       ).one(DEFAULT, 'c')

        # test rebuild url
        vol3 = vol2.one(
                        DEFAULT,
                        'a',
                        rebuild_url=True
                        ).one(
                              DEFAULT,
                              'b'
                              ).all(DEFAULT)

        self.assertIsInstance(vol1, Resource)
        self.assertIsInstance(vol2, Resource)
        self.assertIsInstance(vol3, Resource)

        self.assertIsInstance(vol1.parent, Resource)
        self.assertIsInstance(vol2.parent, Resource)
        self.assertIsInstance(vol3.parent, Resource)

        self.assertEqual(vol1.url, self.base_url + url1)
        self.assertEqual(vol2.url, self.base_url + url2)
        self.assertEqual(vol3.url, self.base_url + url1)

    @httpretty.activate
    def test_toUrl(self):
        domain = self.client.domain
        url = '/default/a/default/b/default/c'
        method = 'attach'
        body = {'test': 'test'}
        httpretty.register_uri(httpretty.GET,
                               domain + self.base_url + url + '/' + method,
                               body=custom_method_get_json,
                               content_type='application/json')
        httpretty.register_uri(httpretty.POST,
                               domain + self.base_url + url + '/' + method,
                               body=action_response_json,
                               content_type='application/json')
        vol = self.resource.one(
                                DEFAULT,
                                'a'
                                ).one(
                                      DEFAULT,
                                      'b'
                                      ).one(DEFAULT, 'c')
        _, body1 = vol.toUrl(method)
        self.assertEqual(vol.url, self.base_url + url)
        self.assertEqual(body1, custom_method_get)

        _, body2 = vol.toUrl(method, body)
        self.assertEqual(vol.url, self.base_url + url)
        self.assertEqual(body2, action_response['server'])

    @httpretty.activate
    def test_create_from_template_and_save(self):
        domain = self.client.domain
        url = '/default/a/default/b/default'
        httpretty.register_uri(
            httpretty.POST,
            domain + self.base_url + url,
            responses=[
                httpretty.Response(
                    body=action_response_json,
                    content_type='application/json',
                    adding_headers={
                        'Location': self.base_url + url + '/vol1_id'
                    },
                    status=201),
                httpretty.Response(
                    body=action_response_json,
                    content_type='application/json',
                    adding_headers={
                        'Location': self.base_url + url + '/vol2_id'
                    },
                    status=201),
                httpretty.Response(
                    body=action_response_json,
                    content_type='application/json',
                    adding_headers={
                        'Location': self.base_url + url + '/vol3_id'
                    },
                    status=201),
            ]
        )
        httpretty.register_uri(
            httpretty.PUT,
            domain + self.base_url + url + '/vol3_id',
            responses=[
                httpretty.Response(
                    body=action_response_json,
                    content_type='application/json',
                    adding_headers={
                        'Location': self.base_url + url + '/vol3_id'
                    },
                    status=201),
            ]
        )
        vol1 = self.resource.one(
            DEFAULT,
            'a'
            ).one(DEFAULT,
                  'b'
                  ).all(DEFAULT).create_from_template(default_template)
        self.assertIsInstance(vol1, Resource)
        self.assertIsInstance(vol1.manager, DefaultManager)
        self.assertEqual(vol1.name, default_template['name'])
        self.assertEqual(vol1.url, self.base_url + url)
        self.assertEqual(vol1.representation, default_template)
        resp1, data1 = vol1.save()
        self.assertIsInstance(data1[0], Resource)
        self.assertEqual(resp1.status_code, 201)
        self.assertEqual(resp1.headers['Location'],
                         self.base_url + url + '/vol1_id'
                         )
        self.assertEqual(resp1.headers['Location'], vol1.url)

        vol2 = self.resource.one(
                                 DEFAULT,
                                 'a'
                                 ).one(
                                       DEFAULT,
                                       'b'
                                       ).one(
                                             DEFAULT,
                                             'c'
                                       ).create_from_template(default_template)
        vol2._template = default_template
        vol2.name = 'vol2'
        self.assertIsInstance(vol2, Resource)
        self.assertIsInstance(vol2.manager, DefaultManager)
        self.assertEqual(vol2.name, 'vol2')
        self.assertEqual(vol2.url, self.base_url + url)
        rep = default_template.copy()
        rep.update({'name': 'vol2'})
        self.assertEqual(vol2.representation, rep)
        resp2, data2 = vol2.save()
        self.assertIsInstance(data2[0], Resource)
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp2.headers['Location'],
                         self.base_url + url + '/vol2_id'
                         )
        self.assertEqual(resp2.headers['Location'], vol2.url)

        rep_with_id = default_template.copy()
        rep_with_id.update({'name': 'vol3', 'id': 'vol3_id'})
        vol3 = self.resource.one(
            DEFAULT,
            'a'
            ).one(DEFAULT,
                  'b'
                  ).one(DEFAULT,
                        'c'
                        ).create_from_template(rep_with_id)
        self.assertIsInstance(vol3, Resource)
        self.assertIsInstance(vol3.manager, DefaultManager)
        self.assertEqual(vol3.name, 'vol3')
        self.assertEqual(vol3.id, 'vol3_id')
        self.assertEqual(vol3.url, self.base_url + url + '/vol3_id')
        self.assertEqual(vol3.representation, rep_with_id)
        resp3, data3 = vol3.save()
        # default create method is put if id is specified.
        self.assertEqual(data3, action_response.get('server'))
        self.assertEqual(resp3.status_code, 201)
        self.assertEqual(resp3.headers['Location'],
                         self.base_url + url + '/vol3_id'
                         )

    def test_create(self):
        pass

    @httpretty.activate
    def test_lazy_loading(self):
        domain = self.client.domain
        url_list = '/default'
        vol_id = default_a_response['data']['default'][0]['id']
        url_a = '/default/{}'.format(vol_id)
        httpretty.register_uri(httpretty.GET,
                               domain + self.base_url + url_list,
                               body=default_list_response_json,
                               content_type='application/json')
        httpretty.register_uri(httpretty.GET,
                               domain + self.base_url + url_a,
                               body=default_a_response_json,
                               content_type='application/json')

        de_list = self.resource.all(DEFAULT).list()
        de0 = de_list[0]
        self.assertIsInstance(de0, Resource)
        self.assertIsInstance(de0.manager, DefaultManager)
        de0._template = {'id': '', 'name': ''}
        self.assertEqual(
                         de0.id,
                         default_list_response['data']['default'][0]['id']
                         )
        self.assertFalse('name' in de0.representation)
        # 'unknown' is not in _template
        self.assertRaises(AttributeError, getattr, de0, 'unknown')
        self.assertFalse(de0.is_loaded())
        # loading details
        self.assertEqual(
                         de0.name,
                         default_a_response['data']['default'][0]['name']
                         )
        self.assertTrue('name' in de0.representation)
        self.assertTrue(de0.is_loaded())

    def test_get_url(self):
        self.assertEqual(self.resource._get_url('/test'), '/test')
        self.assertEqual(self.resource._get_url(
                                        {'rel': 'self', 'href': '/test'}),
                         '/test'
                         )
        self.assertEqual(self.resource._get_url(
                                    [{'rel': 'self', 'href': '/test'},
                                     {'rel': 'bookmark',
                                      'href': '/bookmark'}, ]),
                         '/test'
                         )
        self.assertEqual(self.resource._get_url(
                                    [{'rel': 'self_', 'href': '/test'},
                                     {'rel': 'bookmark',
                                      'href': '/bookmark'}, ]),
                         ''
                         )
        self.assertEqual(self.resource._get_url(
                                    [{'rel': 'self', 'href_': '/test'},
                                     {'rel': 'bookmark',
                                      'href_': '/bookmark'}, ]),
                         ''
                         )
        self.assertEqual(self.resource._get_url(
                                    [{'rel_': 'self', 'href': '/test'},
                                     {'rel_': 'bookmark',
                                      'href': '/bookmark'}, ]),
                         ''
                         )
        self.assertRaises(Exception, self.resource._get_url, object())

    def test_id(self):
        self.assertFalse(hasattr(self.resource, 'id'))
        self.assertFalse(hasattr(self.resource, '_id'))
        self.resource._add_details(info)
        self.assertTrue(hasattr(self.resource, 'id'))
        self.assertTrue(hasattr(self.resource, '_id'))

        def set_id(_id):
            self.resource.id = _id
        self.assertRaises(Exception, set_id, 'a')

    def test_modified_info_dict(self):
        re = Resource(self.client, DefaultManager(self.client))
        self.assertEqual(re._get_modified_info_dict(), {})
        re._set_modified_info_dict('key1', 'val1')
        self.assertEqual(re._get_modified_info_dict(), {'key1': 'val1'})
        re._del_modified_info_dict_key('key')
        self.assertEqual(re._get_modified_info_dict(), {'key1': 'val1'})
        re._del_modified_info_dict_key('key1')
        self.assertEqual(re._get_modified_info_dict(), {})
        re._set_modified_info_dict('key2', 'val2')
        self.assertEqual(re._get_modified_info_dict(), {'key2': 'val2'})
        re._del_modified_info_dict_keys({'key1': 'val1'})
        self.assertEqual(re._get_modified_info_dict(), {'key2': 'val2'})
        re._del_modified_info_dict_keys({'key2': 'val2'})
        self.assertEqual(re._get_modified_info_dict(), {})

        re1 = Resource(self.client,
                       DefaultManager(self.client),
                       )
        re1._template = {'key1': '', 'key2': ''}
        re1._add_details(info={'key1': 'val1'})
        self.assertEqual(re1._get_modified_info_dict(), {})
        self.assertEqual(re1.key1, 'val1')
        re1.key1 = 'val1_changed'
        self.assertEqual(
                         re1._get_modified_info_dict(),
                         {'key1': 'val1_changed'}
                         )
        self.assertEqual(re1.key1, 'val1_changed')

        # set attr not in _template
        re1.key3 = 'val3'
        self.assertEqual(
                         re1._get_modified_info_dict(),
                         {'key1': 'val1_changed'}
                         )

    def test_force_get(self):
        re1 = Resource(self.client,
                       DefaultManager(self.client),
                       )
        re1._template = {'key1': '', 'key2': ''}
        re1._add_details(info={'key1': 'val1'})
        self.assertEqual(re1._get_modified_info_dict(), {})
        self.assertEqual(re1.key1, 'val1')
        re1.key1 = 'val1_changed'
        self.assertEqual(
                         re1._get_modified_info_dict(),
                         {'key1': 'val1_changed'}
                         )
        self.assertEqual(re1.key1, 'val1_changed')

        re1._add_details(info={'key1': 'val1'})
        self.assertEqual(re1.key1, 'val1_changed')

        re1._add_details(info={'key1': 'val1'}, force=True)
        self.assertEqual(re1.key1, 'val1')

    @httpretty.activate
    def test_list(self):
        domain = self.client.domain
        url = '/default'
        url1 = default_a_response['data']['default'][0]['link']['href']
        httpretty.register_uri(httpretty.GET, domain + self.base_url + url,
                               body=default_list_response_json,
                               content_type='application/json')
        httpretty.register_uri(httpretty.GET, domain + url1,
                               body=default_a_response_json,
                               content_type='application/json')

        vol = self.resource.all(DEFAULT)
        self.assertEqual(vol.url, self.base_url + url)
        self.assertRaises(AttributeError, getattr, vol, 'id')
        vol_list = vol.list()
        self.assertIsInstance(vol_list, list)
        vol1 = vol_list[0]
        self.assertEqual(
                    vol1.url,
                    default_list_response['data']['default'][0]['link']['href']
                         )
        self.assertEqual(
                         vol1.id,
                         default_a_response['data']['default'][0]['id']
                         )

        # lazy loading
        vol1._template = {'id': '', 'name': ''}
        self.assertEqual(
                         vol1.name,
                         default_a_response['data']['default'][0]['name']
                         )

    @httpretty.activate
    def test_get(self):
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        httpretty.register_uri(httpretty.GET, domain + url,
                               body=default_a_response_json,
                               content_type='application/json')

        vol = self.resource.one(DEFAULT, vol_id)
        self.assertEqual(vol.url, url)
        self.assertEqual(vol.id, vol_id)
        vol.get()
        self.assertEqual(
                    vol.url,
                    default_a_response['data']['default'][0]['link']['href']
                         )
        self.assertEqual(
                         vol.name,
                         default_a_response['data']['default'][0]['name']
                         )

        vol1 = self.resource.all(DEFAULT).get(vol_id)
        self.assertEqual(
                    vol1.url,
                    default_a_response['data']['default'][0]['link']['href']
                         )
        self.assertEqual(
                         vol1.name,
                         default_a_response['data']['default'][0]['name']
                         )

    @httpretty.activate
    def test_post(self):
        # post append: tested in test_create_from_template_and_save

        # post: tested in test_toUrl
        pass

    @httpretty.activate
    def test_put(self):
        # put new: tested in test_create_from_template_and_save

        # put update:
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        httpretty.register_uri(httpretty.GET, domain + url,
                               body=default_a_response_json,
                               content_type='application/json')
        httpretty.register_uri(httpretty.PUT, domain + url,
                               body=json.dumps({'status': 'updated'}),
                               content_type='application/json',
                               status=200)

        vol = self.resource.one(DEFAULT, vol_id).get()
        self.assertEqual(vol.name,
                         default_a_response['data']['default'][0]['name']
                         )
        vol.name = 'vol1_rename'
        resp, data = vol.put()
        self.assertEqual(data, {'status': 'updated'})
        self.assertEqual(resp.status_code, 200)

    @httpretty.activate
    def test_patch(self):
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        httpretty.register_uri(httpretty.GET, domain + url,
                               body=default_a_response_json,
                               content_type='application/json')
        httpretty.register_uri(httpretty.PATCH, domain + url,
                               body=json.dumps({'status': 'updated'}),
                               content_type='application/json',
                               status=200)

        vol = self.resource.one(DEFAULT, vol_id).get()
        self.assertEqual(
                         vol.name,
                         default_a_response['data']['default'][0]['name']
                         )
        vol._template = default_template
        vol.name = 'vol1_rename_patch'
        self.assertEqual(
                         vol._get_modified_info_dict(),
                         {'name': 'vol1_rename_patch'}
                         )
        resp, data = vol.patch()
        self.assertEqual(data, {'status': 'updated'})
        self.assertEqual(resp.status_code, 200)

    @httpretty.activate
    def test_delete(self):
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        httpretty.register_uri(httpretty.GET, domain + url,
                               body=default_a_response_json,
                               content_type='application/json')
        httpretty.register_uri(httpretty.DELETE, domain + url,
                               content_type='application/json',
                               status=204)

        vol = self.resource.one(DEFAULT, vol_id).get()
        self.assertEqual(
                         vol.name,
                         default_a_response['data']['default'][0]['name']
                         )
        resp, data = vol.delete()
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(data, DEFAULT_SUCCESS_BODY_DICT)

    def test_save(self):
        # save new: tested in test_create_from_template_and_save

        # save update: tested in test_put
        pass

    def test_update(self):
        # update put: tested in test_put

        # update patch: tested in test_patch
        pass

    def test_equal(self):
        re1 = Resource(self.client, resource_id='test')
        re2 = Resource(self.client, resource_id='test')
        re3 = Resource(self.client, resource_id='test3')
        self.assertTrue(re1 == re2)
        self.assertFalse(re1 == re3)
        self.assertFalse(re1 is re2)
        self.assertTrue(re1 in [re2])

    def test_update_list_field(self):
        re1 = Resource(self.client, resource_id='test')
        re1.re_list = [Resource(self.client, resource_id='test{}'.format(n))
                       for n in range(10)
                       ]
        re_not_in = Resource(self.client, resource_id='test11')
        re_in = Resource(self.client, resource_id='test1')
        with self.assertRaises(KeyError):
            re1._update_list_field('re_list', re_not_in, '-')
        with self.assertRaises(KeyError):
            re1._update_list_field('re_list', re_in)
        re1._update_list_field('re_list', re_not_in)
        self.assertTrue(re_not_in in re1.re_list)
        re1._update_list_field('re_list', re_in, '-')
        self.assertTrue(re_in not in re1.re_list)
