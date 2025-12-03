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
import re
from http import HTTPStatus

import pytest
import responses

from pyds8k import messages
from pyds8k.base import DefaultManager, Resource
from pyds8k.messages import DEFAULT_SUCCESS_BODY_DICT

from . import base
from .data import (
    action_response,
    action_response_json,
    default_template,
    get_response_data_by_type,
    get_response_json_by_type,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

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
        super().setUp()

    def test_one_all(self):
        url1 = '/default/a/default/b/default'
        url2 = '/default/a/default/b/default/c'
        vol1 = self.resource.one(DEFAULT, 'a').one(DEFAULT, 'b').all(DEFAULT)
        vol2 = self.resource.one(DEFAULT, 'a').one(DEFAULT, 'b').one(DEFAULT, 'c')

        # test rebuild url
        vol3 = vol2.one(DEFAULT, 'a', rebuild_url=True).one(DEFAULT, 'b').all(DEFAULT)

        assert isinstance(vol1, Resource)
        assert isinstance(vol2, Resource)
        assert isinstance(vol3, Resource)

        assert isinstance(vol1.parent, Resource)
        assert isinstance(vol2.parent, Resource)
        assert isinstance(vol3.parent, Resource)

        assert vol1.url == url1
        assert vol2.url == url2
        assert vol3.url == url1

    @responses.activate
    def test_toUrl(self):  # noqa: N802
        domain = self.client.domain
        url = '/default/a/default/b/default/c'
        method = 'attach'
        body = {'test': 'test'}
        responses.get(
            domain + self.base_url + url + '/' + method,
            body=custom_method_get_json,
            content_type='application/json',
        )
        responses.post(
            domain + self.base_url + url + '/' + method,
            body=action_response_json,
            content_type='application/json',
        )
        vol = self.resource.one(DEFAULT, 'a').one(DEFAULT, 'b').one(DEFAULT, 'c')
        _, body1 = vol.toUrl(method)
        assert vol.url == url
        assert body1 == custom_method_get

        _, body2 = vol.toUrl(method, body)
        assert vol.url == url
        assert body2 == action_response['server']

    @responses.activate
    def test_create_from_template_and_save(self):
        domain = self.client.domain
        url = '/default/a/default/b/default'
        responses.post(
            domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            headers={'Location': self.base_url + url + '/vol1_id'},
            status=HTTPStatus.CREATED.value,
        )
        responses.post(
            domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            headers={'Location': self.base_url + url + '/vol2_id'},
            status=HTTPStatus.CREATED.value,
        )
        responses.post(
            domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            headers={'Location': self.base_url + url + '/vol3_id'},
            status=HTTPStatus.CREATED.value,
        )

        responses.put(
            domain + self.base_url + url + '/vol3_id',
            body=action_response_json,
            content_type='application/json',
            headers={'Location': self.base_url + url + '/vol3_id'},
            status=HTTPStatus.CREATED.value,
        )
        vol1 = (
            self.resource.one(DEFAULT, 'a')
            .one(DEFAULT, 'b')
            .all(DEFAULT)
            .create_from_template(default_template)
        )
        assert isinstance(vol1, Resource)
        assert isinstance(vol1.manager, DefaultManager)
        assert vol1.name == default_template['name']
        assert vol1.url == url
        assert vol1.representation == default_template
        resp1, data1 = vol1.save()
        assert isinstance(data1[0], Resource)
        assert resp1.status_code == HTTPStatus.CREATED
        assert resp1.headers['Location'] == self.base_url + url + '/vol1_id'
        assert resp1.headers['Location'] == vol1.url

        vol2 = (
            self.resource.one(DEFAULT, 'a')
            .one(DEFAULT, 'b')
            .one(DEFAULT, 'c')
            .create_from_template(default_template)
        )
        vol2._template = default_template
        vol2.name = 'vol2'
        assert isinstance(vol2, Resource)
        assert isinstance(vol2.manager, DefaultManager)
        assert vol2.name == 'vol2'
        assert vol2.url == url
        rep = default_template.copy()
        rep.update({'name': 'vol2'})
        assert vol2.representation == rep
        resp2, data2 = vol2.save()
        assert isinstance(data2[0], Resource)
        assert resp2.status_code == HTTPStatus.CREATED
        assert resp2.headers['Location'] == self.base_url + url + '/vol2_id'
        assert resp2.headers['Location'] == vol2.url

        rep_with_id = default_template.copy()
        rep_with_id.update({'name': 'vol3', 'id': 'vol3_id'})
        vol3 = (
            self.resource.one(DEFAULT, 'a')
            .one(DEFAULT, 'b')
            .one(DEFAULT, 'c')
            .create_from_template(rep_with_id)
        )
        assert isinstance(vol3, Resource)
        assert isinstance(vol3.manager, DefaultManager)
        assert vol3.name == 'vol3'
        assert vol3.id == 'vol3_id'
        assert vol3.url == url + '/vol3_id'
        assert vol3.representation == rep_with_id
        resp3, data3 = vol3.save()
        # default create method is put if id is specified.
        assert data3 == action_response.get('server')
        assert resp3.status_code == HTTPStatus.CREATED
        assert resp3.headers['Location'] == self.base_url + url + '/vol3_id'

    def test_create(self):
        pass

    @responses.activate
    def test_lazy_loading(self):
        domain = self.client.domain
        url_list = '/default'
        vol_id = default_a_response['data']['default'][0]['id']
        url_a = f'/default/{vol_id}'
        responses.get(
            domain + self.base_url + url_list,
            body=default_list_response_json,
            content_type='application/json',
        )
        responses.get(
            domain + self.base_url + url_a,
            body=default_a_response_json,
            content_type='application/json',
        )

        de_list = self.resource.all(DEFAULT).list()
        de0 = de_list[0]
        assert isinstance(de0, Resource)
        assert isinstance(de0.manager, DefaultManager)
        de0._template = {'id': '', 'name': ''}
        assert de0.id == default_list_response['data']['default'][0]['id']
        assert 'name' not in de0.representation
        # 'unknown' is not in _template
        with pytest.raises(AttributeError):
            de0.uknown  # noqa: B018 Testing only that exception raised

        assert not de0.is_loaded()
        # loading details
        assert de0.name == default_a_response['data']['default'][0]['name']
        assert 'name' in de0.representation
        assert de0.is_loaded()

    def test_get_url(self):
        assert self.resource._get_url('/test') == '/test'
        assert self.resource._get_url({'rel': 'self', 'href': '/test'}) == '/test'
        assert (
            self.resource._get_url(
                [
                    {'rel': 'self', 'href': '/test'},
                    {'rel': 'bookmark', 'href': '/bookmark'},
                ]
            )
            == '/test'
        )
        assert (
            self.resource._get_url(
                [
                    {'rel': 'self_', 'href': '/test'},
                    {'rel': 'bookmark', 'href': '/bookmark'},
                ]
            )
            == ''
        )
        assert (
            self.resource._get_url(
                [
                    {'rel': 'self', 'href_': '/test'},
                    {'rel': 'bookmark', 'href_': '/bookmark'},
                ]
            )
            == ''
        )
        assert (
            self.resource._get_url(
                [
                    {'rel_': 'self', 'href': '/test'},
                    {'rel_': 'bookmark', 'href': '/bookmark'},
                ]
            )
            == ''
        )
        with pytest.raises(Exception, match=messages.CAN_NOT_GET_URL):
            self.resource._get_url(object())

    def test_id(self):
        assert not hasattr(self.resource, 'id')
        assert not hasattr(self.resource, '_id')
        self.resource._add_details(info)
        assert hasattr(self.resource, 'id')
        assert hasattr(self.resource, '_id')

        def set_id(_id):
            self.resource.id = _id

        with pytest.raises(Exception, match=re.escape("The field id is read only.")):
            set_id('a')

    def test_modified_info_dict(self):
        re = Resource(self.client, DefaultManager(self.client))
        assert re._get_modified_info_dict() == {}
        re._set_modified_info_dict('key1', 'val1')
        assert re._get_modified_info_dict() == {'key1': 'val1'}
        re._del_modified_info_dict_key('key')
        assert re._get_modified_info_dict() == {'key1': 'val1'}
        re._del_modified_info_dict_key('key1')
        assert re._get_modified_info_dict() == {}
        re._set_modified_info_dict('key2', 'val2')
        assert re._get_modified_info_dict() == {'key2': 'val2'}
        re._del_modified_info_dict_keys({'key1': 'val1'})
        assert re._get_modified_info_dict() == {'key2': 'val2'}
        re._del_modified_info_dict_keys({'key2': 'val2'})
        assert re._get_modified_info_dict() == {}

        re1 = Resource(
            self.client,
            DefaultManager(self.client),
        )
        re1._template = {'key1': '', 'key2': ''}
        re1._add_details(info={'key1': 'val1'})
        assert re1._get_modified_info_dict() == {}
        assert re1.key1 == 'val1'
        re1.key1 = 'val1_changed'
        assert re1._get_modified_info_dict() == {'key1': 'val1_changed'}
        assert re1.key1 == 'val1_changed'

        # set attr not in _template
        re1.key3 = 'val3'
        assert re1._get_modified_info_dict() == {'key1': 'val1_changed'}

    def test_force_get(self):
        re1 = Resource(
            self.client,
            DefaultManager(self.client),
        )
        re1._template = {'key1': '', 'key2': ''}
        re1._add_details(info={'key1': 'val1'})
        assert re1._get_modified_info_dict() == {}
        assert re1.key1 == 'val1'
        re1.key1 = 'val1_changed'
        assert re1._get_modified_info_dict() == {'key1': 'val1_changed'}
        assert re1.key1 == 'val1_changed'

        re1._add_details(info={'key1': 'val1'})
        assert re1.key1 == 'val1_changed'

        re1._add_details(info={'key1': 'val1'}, force=True)
        assert re1.key1 == 'val1'

    @responses.activate
    def test_list(self):
        domain = self.client.domain
        url = '/default'
        url1 = default_a_response['data']['default'][0]['link']['href']
        responses.get(
            domain + self.base_url + url,
            body=default_list_response_json,
            content_type='application/json',
        )
        responses.get(
            domain + self.base_url + url1,
            body=default_a_response_json,
            content_type='application/json',
        )

        vol = self.resource.all(DEFAULT)
        assert vol.url == url
        with pytest.raises(AttributeError):
            vol.id  # noqa: B018 Testing only that exception raised
        vol_list = vol.list()
        assert isinstance(vol_list, list)
        vol1 = vol_list[0]
        assert vol1.url == default_list_response['data']['default'][0]['link']['href']
        assert vol1.id == default_a_response['data']['default'][0]['id']

        # lazy loading
        vol1._template = {'id': '', 'name': ''}
        assert vol1.name == default_a_response['data']['default'][0]['name']

    @responses.activate
    def test_get(self):
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        responses.get(
            domain + self.base_url + url,
            body=default_a_response_json,
            content_type='application/json',
        )

        vol = self.resource.one(DEFAULT, vol_id)
        assert vol.url == url
        assert vol.id == vol_id
        vol.get()
        assert vol.url == default_a_response['data']['default'][0]['link']['href']
        assert vol.name == default_a_response['data']['default'][0]['name']

        vol1 = self.resource.all(DEFAULT).get(vol_id)
        assert vol1.url == default_a_response['data']['default'][0]['link']['href']
        assert vol1.name == default_a_response['data']['default'][0]['name']

    @responses.activate
    def test_post(self):
        # post append: tested in test_create_from_template_and_save

        # post: tested in test_toUrl
        pass

    @responses.activate
    def test_put(self):
        # put new: tested in test_create_from_template_and_save

        # put update:
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        responses.get(
            domain + self.base_url + url,
            body=default_a_response_json,
            content_type='application/json',
        )
        responses.put(
            domain + self.base_url + url,
            body=json.dumps({'status': 'updated'}),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        vol = self.resource.one(DEFAULT, vol_id).get()
        assert vol.name == default_a_response['data']['default'][0]['name']
        vol.name = 'vol1_rename'
        resp, data = vol.put()
        assert data == {'status': 'updated'}
        assert resp.status_code == HTTPStatus.OK

    @responses.activate
    def test_patch(self):
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        responses.get(
            domain + self.base_url + url,
            body=default_a_response_json,
            content_type='application/json',
        )
        responses.patch(
            domain + self.base_url + url,
            body=json.dumps({'status': 'updated'}),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        vol = self.resource.one(DEFAULT, vol_id).get()
        assert vol.name == default_a_response['data']['default'][0]['name']
        vol._template = default_template
        vol.name = 'vol1_rename_patch'
        assert vol._get_modified_info_dict() == {'name': 'vol1_rename_patch'}
        resp, data = vol.patch()
        assert data == {'status': 'updated'}
        assert resp.status_code == HTTPStatus.OK

    @responses.activate
    def test_delete(self):
        domain = self.client.domain
        url = default_a_response['data']['default'][0]['link']['href']
        vol_id = default_a_response['data']['default'][0]['id']
        responses.get(
            domain + self.base_url + url,
            body=default_a_response_json,
            content_type='application/json',
        )
        responses.delete(
            domain + self.base_url + url,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        vol = self.resource.one(DEFAULT, vol_id).get()
        assert vol.name == default_a_response['data']['default'][0]['name']
        resp, data = vol.delete()
        assert resp.status_code == HTTPStatus.OK
        assert data == DEFAULT_SUCCESS_BODY_DICT

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
        assert re1 == re2
        assert re1 != re3
        assert re1 is not re2
        assert re1 in [re2]

    def test_update_list_field(self):
        re1 = Resource(self.client, resource_id='test')
        re1.re_list = [Resource(self.client, resource_id=f'test{n}') for n in range(10)]
        re_not_in = Resource(self.client, resource_id='test11')
        re_in = Resource(self.client, resource_id='test1')
        with pytest.raises(KeyError):
            re1._update_list_field('re_list', re_not_in, '-')
        with pytest.raises(KeyError):
            re1._update_list_field('re_list', re_in)
        re1._update_list_field('re_list', re_not_in)
        assert re_not_in in re1.re_list
        re1._update_list_field('re_list', re_in, '-')
        assert re_in not in re1.re_list
