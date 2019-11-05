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
from importlib import import_module
from . import messages
from pyds8k.utils import get_response_parser_class, \
    get_request_parser_class
from pyds8k.utils import is_absolute_url
from pyds8k.utils import HTTP200, HTTP204, POSTA, POST
from pyds8k.exceptions import URLNotSpecifiedError, \
    FieldReadOnly, \
    URLParseError, \
    ResponseBodyMissingError
from pyds8k import PYDS8K_DEFAULT_LOGGER
from logging import getLogger

logger = getLogger(PYDS8K_DEFAULT_LOGGER)
get_resource_by_route = None


class URLBuilderMixin(object):
    def one(self, route, resource_id):
        pass

    def all(self, route):
        pass


class UtilsMixin(object):
    def _update_list_field(self, field_name, value_list, operator='+'):
        if not isinstance(value_list, list):
            value_list = [value_list]
        field = getattr(self, field_name)
        if operator == '+':
            for item in value_list:
                if item in field:
                    raise KeyError(
                        messages.ITEM_IN_LIST.format(field_name, item)
                        )
                field.append(item)
        if operator == '-':
            for item in value_list:
                if item not in field:
                    raise KeyError(
                        messages.ITEM_NOT_IN_LIST.format(field_name, item)
                        )
                field.pop(field.index(item))
        return field

    def _get_id(self):
        return self.id if hasattr(self, 'id') else id(self)

    def remove_None_fields_from_dict(self, input_dict):
        new_dict = {}
        for (key, value) in input_dict.items():
            if value is not None:
                new_dict[key] = value
        return new_dict


class BaseResource(object):
    pass


class Resource(UtilsMixin, BaseResource):
    """
    A resource represents a particular representation of
    a resource state or a application state.

    :param client: HTTPClient object
    :param manager: Manager object
    :param url: A resource or a resource collection's url
    :param info: Dictionary representing resource attributes
    :param resource_id: The resource's id
    :param parent: The parent resource object
    :param loaded: All details is loaded if set to True
    """

    id_field = 'id'
    url_field = 'link'
    # The HTTP method when creating new resource
    create_method = 'put'
    # base_url must to set to empty string in this base class
    base_url = ''
    # Set the value to None if the field is not required when creation.
    _template = {}
    related_resource = {}
    alias = {}

    def __init__(self, client, manager=None, url='', info={},
                 resource_id=None, parent=None, loaded=False):
        self.set_loaded(loaded)
        self._start_init()
        self._init_updating()
        self.ResponseParser = get_response_parser_class(client.service_type)
        self.manager = manager
        if self.manager:
            self.manager.managed_object = self
        self.client = client
        self.representation = {}
        self.url = self._add_base_to_url(url)
        if resource_id:
            self._id = resource_id
        self.parent = parent
        self._custom_url = ''
        self._set_modified_info_dict()
        if info:
            self._add_details(info)
        self._finish_init()

    def one(self, route, resource_id, rebuild_url=False):
        global get_resource_by_route
        if not get_resource_by_route:
            get_resource_by_route = \
                import_module('{}.resources.utils'.format(__package__)
                              ).get_resource_by_route
        url = self._set_url(route, resource_id, rebuild_url=rebuild_url)
        return get_resource_by_route(route, self.client,
                                     url, self, resource_id)

    def all(self, route, rebuild_url=False):
        global get_resource_by_route
        if not get_resource_by_route:
            get_resource_by_route = \
                import_module('{}.resources.utils'.format(__package__)
                              ).get_resource_by_route
        url = self._set_url(route, rebuild_url=rebuild_url)
        return get_resource_by_route(route, self.client, url, self)

    def toUrl(self, method, body={}):
        """
        To send non-standard rest request, like /attach
        """

        self._set_custom_url(method)
        if body:
            resp, res_body = self.post(body=body)
        else:
            resp, res_body = self.get_response()
        self._reverse_custom_url()
        return resp, res_body

    def custom_method(self, para1, para2):
        """
        Like customUrl(), but use a particular method name instand of url.
        """

        result = None
        if not self._custom_url:
            result = self.manager.custom_method(para1, para2)
        else:
            result = self.get(para1, para2)  # or post, put, ...
            self._reverse_custom_url()
        return result

    def create(self, **kwargs):
        custom_info = {}
        # for (k, v) in six.iteritems(info):
        for (k, v) in kwargs.items():
            if k in list(self._template.keys()):
                custom_info[k] = v
        return self.create_from_template(custom_info)

    def create_from_template(self, custom_info={}):
        _url = self._rm_id_in_url()
        _info = self._template.copy()
        if self.id_field in _info:
            del _info[self.id_field]
        _info.update(custom_info)
        data = self.remove_None_fields_from_dict(_info)

        res = self.__class__(client=self.client,
                             manager=self.manager.__class__(self.client),
                             url=_url,
                             info=data,
                             parent=self.parent,
                             # Set loaded=True to avoid lazy-loading
                             loaded=True)
        for key, value in data.items():
            if value:
                res._set_modified_info_dict(key, value)
        res._is_new = True
        return res

    def _update_alias(self, res):
        for key, alias in self.alias.items():
            if key in res:
                res[alias] = res.pop(key)
        return res

    def _set_url(self, route, resource_id='',  rebuild_url=False):
        url = self.url if not rebuild_url else ''
        if resource_id:
            url += '/{}/{}'.format(route, resource_id)
        else:
            url += '/{}'.format(route)
        return url

    def _add_id_to_url(self, resource_id):
        if not self.url.endswith('/{}'.format(resource_id)):
            self.url += '/{}'.format(resource_id)

    def _rm_id_in_url(self, resource_id=''):
        if not hasattr(self, 'id'):
            return self.url
        res_id = resource_id or self.id
        if self.url.endswith('/{}'.format(res_id)):
            return self.url[:len(self.url) - len(self.id) - 1]
        return self.url

    def _add_base_to_url(self, url):
        if (self.base_url not in url) and (not is_absolute_url(url)):
            return self.base_url + url
        return url

    def _set_custom_url(self, url):
        self._custom_url = self.url + '/' + url
        self._url_backup = self.url
        self.url = self._custom_url

    def _reverse_custom_url(self):
        if self._custom_url:
            self._custom_url = ''
            self.url = self._url_backup

    def _add_details(self, info, force=False):
        self._start_updating()
        info = self._update_alias(info)
        try:
            # set id field first.
            self._id = info[self.id_field]
        except KeyError:
            pass

        self_url = self.ResponseParser.get_link_from_representation(info)
        if self_url:
            self.url = self_url
        # for (k, v) in six.iteritems(info):
        for (k, v) in info.items():
            if not force and k in list(self._modified_info_dict.keys()):
                continue
            if not k == self.id_field:
                setattr(self, k, v)
            self.representation[k] = v

        for related_key in list(self.related_resource.keys()):
            if related_key[1:] in self.representation:
                self._set_related_resource(related_key[1:])

        self._stop_updating()

    def _set_related_resource(self, res_key):
        # Related resources is set during loading details, and are readonly,
        # If you want to change it, you should set the attr with the same
        # name(without '_'), then update it to server and load details again.
        try:
            res_info = self.representation[res_key]
            res_class, res_manager = self.related_resource.get('_' + res_key)
            res_id = res_info[res_class.id_field]
            self.representation[res_key] = res_id
            setattr(self, res_key, res_id)
            setattr(self,
                    '_' + res_key,
                    res_class(self.client,
                              manager=res_manager(self.client),
                              resource_id=res_id,
                              info=res_info,
                              loaded=False,
                              )
                    )
        except Exception:
            logger.debug(
                messages.SET_RELATED_RESOURCE_FAILED.format(res_key, self)
                )
            self.representation[res_key] = res_info
            setattr(self, res_key, res_info)
            setattr(self, '_' + res_key, None)

    def _get_url(self, urls):
        if isinstance(urls, str):
            return urls
        elif isinstance(urls, dict):
            urls = [urls]
        elif isinstance(urls, list):
            pass
        else:
            raise URLParseError()
        for url in urls:
            if url.get('rel') == 'self':
                return url.get('href', '')
        return ''

    def __getattr__(self, k):
        if k == 'id' or k == self.id_field:
            if '_id' not in self.__dict__:
                raise AttributeError(k)
            else:
                return self._id
        # If we can get the attr from a resource collection
        # we don't need to get the resource details.
        # So we don't load the details until an attr which is
        # not in the resource collection is required.
        if k not in self.__dict__:
            if k in self._template and not self.is_loaded():
                self.get()
                return getattr(self, k)

            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def __setattr__(self, key, value):
        if key == '_id':
            self._add_id_to_url(value)
        if key.startswith('_'):
            super(Resource, self).__setattr__(key, value)
            return
        if self._is_init():
            return super(Resource, self).__setattr__(key, value)
        if key == 'id' or key == self.id_field:
            raise FieldReadOnly(key)
        if not self.is_updating() and (key in self._template or key in self.representation):  # noqa
            self.representation[key] = value
            self._set_modified_info_dict(key, value)
        super(Resource, self).__setattr__(key, value)

    def __repr__(self):
        reprkeys = \
            sorted(k for k in self.__dict__ if not str(k).startswith('_') and
                   k not in ('manager', 'client')
                   )
        info = ", ".join("{0}={1}".format(k, getattr(self, k))
                         for k in reprkeys)
        return "<{0} {1}>".format(self.__class__.__name__, info)

    def get(self, resource_id='', force=False, **kwargs):
        self.set_loaded(True)
        if resource_id:
            return self.manager.get(resource_id, **kwargs)
        else:
            _, info = self.manager.get(**kwargs)
            self._add_details(info, force)
            return self

    def get_response(self):
        return self.manager.get()

    def list(self, **kwargs):
        return self.manager.list(**kwargs)

    def put(self):
        resp, data = self.manager.put()
        self._set_modified_info_dict()
        return resp, data

    def patch(self):
        resp, data = self.manager.patch()
        self._set_modified_info_dict()
        return resp, data

    def post(self, body, url=None):
        resp, data = self.manager.post(body=body)
        return resp, data

    def posta(self, body=None):
        _url = self._rm_id_in_url()
        resp, resources = self.manager.posta(url=_url, body=body)
        self._set_modified_info_dict()
        return resp, resources

    def delete(self):
        resp, data = self.manager.delete()
        return resp, data

    def update(self, info={}):
        resp = None
        data = None
        if info:
            resp, data = self.manager.patch(body=info)
            self._del_modified_info_dict_keys(info)
        else:
            resp, data = self.manager.patch(body=self._get_modified_info_dict()
                                            )
            self._set_modified_info_dict()
        return resp, data

    def save(self):
        resp = None
        data = None
        if hasattr(self, 'id'):
            # TODO: I don't like _is_new and create_method, need a better idea.
            if (not hasattr(self, '_is_new')) or (not self._is_new):
                resp, data = self.put()
            else:
                if self.create_method.lower() not in ('posta', 'put'):
                    raise Exception(
                        "You should use POSTA or PUT method to create new resources"  # noqa
                    )
                resp, data = getattr(self, self.create_method.lower())()
                if self.create_method.lower() == 'posta':
                    if isinstance(data[0], Resource):
                        # re-init the res object according to the returned data
                        self.__init__(
                            client=self.client,
                            manager=self.manager,
                            url=data[0].url,
                            resource_id=data[0].id,
                            info=data[0].representation
                        )
                self._is_new = False
        else:
            resp, data = self.posta()
            if isinstance(data[0], Resource):
                # re-init the res object according to the returned res
                self.__init__(
                    client=self.client,
                    manager=self.manager,
                    url=data[0].url,
                    resource_id=data[0].id,
                    info=data[0].representation
                )

        # self.set_loaded(False)   # Set to false in order to use lazy loading.
        return resp, data

    def _get_modified_info_dict(self):
        return self._modified_info_dict

    def _set_modified_info_dict(self, key=None, value=None):
        if not key:
            self._modified_info_dict = {}
        else:
            self._modified_info_dict[key] = value

    def _del_modified_info_dict_key(self, key):
        if key in list(self._modified_info_dict.keys()):
            del self._modified_info_dict[key]

    def _del_modified_info_dict_keys(self, info=None):
        if not info:
            self._modified_info_dict = {}
        else:
            for key in list(info.keys()):
                self._del_modified_info_dict_key(key)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id
        try:
            return self._info == other._info and self.url == other.url
        except Exception:
            return False

    def is_loaded(self):
        return self._loaded

    def set_loaded(self, is_loaded):
        self._loaded = is_loaded

    def _is_init(self):
        return self._initing

    def _start_init(self):
        self._initing = True

    def _finish_init(self):
        self._initing = False

    def _start_updating(self):
        self._updating = True

    def _stop_updating(self):
        self._updating = False

    def _init_updating(self):
        self._updating = False

    def is_updating(self):
        return self._updating

    @classmethod
    def set_id_field(cls, _id_field):
        cls.id_field = _id_field

    @classmethod
    def set_base_url(cls, base):
        url = base
        if url.endswith('/'):
            url = url[:-1]
        if not url.startswith('/'):
            url = '/' + url
        cls.base_url = url

    @classmethod
    def get_template(cls):
        return cls._template.copy()

    def get_template_from_server(self):
        pass


class BaseManager(object):
    pass


class Manager(UtilsMixin, BaseManager):
    """
    Managers interact with a particular type of API (systems, pools, volumes,
    etc.) and provide CRUD operations for them.

    :param client: HTTPClient object
    :param managed_object: The related resource object
    :param url: A resource or a resource collection's url
    """
    resource_class = Resource
    response_key = 'data'
    resource_type = ''

    def __init__(self, client, managed_object=None, url=''):
        self.client = client
        self.managed_object = managed_object
        self.url = url
        self.ResponseParser = get_response_parser_class(client.service_type)
        self.RequestParser = get_request_parser_class(client.service_type)

    def _get_data(self, response_body, method='', response=None):
        if not method:  # get or list
            if not response_body:
                raise ResponseBodyMissingError()
            res_p = self.ResponseParser(response_body, self.resource_type)
            return res_p.get_representations()
        elif method == POSTA:
            if not response_body:
                raise ResponseBodyMissingError()
            res_p = self.ResponseParser(response_body, self.resource_type)
            return res_p.get_posta_response_data()
        else:
            if response_body:
                try:
                    data = self._get_status_body(response_body)
                except Exception:
                    logger.debug(
                        messages.CAN_NOT_GET_STATUS_BODY.format(
                            method,
                            self.resource_class.__name__
                            )
                        )
                    data = response_body
            elif response.status_code in (HTTP200, HTTP204):
                data = messages.DEFAULT_SUCCESS_BODY_DICT
            else:
                res_id = ''
                try:
                    res_id = self.managed_object.id
                except Exception:
                    res_id = ''
                data = json.loads(
                    messages.DEFAULT_FAIL_BODY_JSON.format(
                        action=method,
                        res_class=self.resource_class.__name__,
                        res_id=res_id
                        )
                    )
            return data

    def _get_status_body(self, response_body):
        res_p = self.ResponseParser(response_body, self.resource_type)
        return res_p.get_status_body()

    def _get_request_data(self, data):
        req = self.RequestParser(data)
        return req.get_request_data()

    def _return_new_resource_by_response_data(self, resp, data, url):
        resource_uri = url or resp.headers.get('Location')
        if resource_uri:
            resource_id = self.ResponseParser.get_resource_id_from_url(
                url=resource_uri,
                resource_type=self.resource_type,
                )
        else:
            resource_id = None
        return self.resource_class(
            client=self.client,
            manager=self.__class__(self.client),
            url=resource_uri,
            resource_id=resource_id,
            info=data
        )

    def _get(self, resource_id='', url='', obj_class=None, **kwargs):
        new = False
        parent = None
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
                parent = self.managed_object.parent
                if resource_id:
                    self.url += '/' + resource_id
                    new = True
            else:
                raise URLNotSpecifiedError()
        else:
            self.url = url
            new = True
        resp, body = self.client.get(self.url, **kwargs)
        data = self._get_data(body)[0]

        if not new:
            return resp, data
        else:
            if obj_class is None:
                obj_class = self.resource_class
            return obj_class(client=self.client,
                             manager=self.__class__(self.client),
                             url=self.url,
                             info=data,
                             parent=parent,
                             loaded=True)

    # if url and obj_class is not none, list the sub collection
    # of current resource.
    def _list(self, url='', obj_class=None, body=None, **kwargs):
        parent = None
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
                parent = self.managed_object.parent
            else:
                raise URLNotSpecifiedError()
        else:
            self.url = url
        if body:
            _, body = self.client.post(self.url, body=body)
        else:
            _, body = self.client.get(self.url, **kwargs)
        if obj_class is None:
            obj_class = self.resource_class
        data = self._get_data(body)

        return [obj_class(client=self.client,
                          manager=self.__class__(self.client),
                          url=self.url,
                          parent=parent,
                          info=res) for res in data if res]

    def _post(self, body, url=None):
        if not url:
            if self.managed_object is not None:
                url = self.managed_object.url
            else:
                raise URLNotSpecifiedError()
        resp, res_body = self.client.post(url,
                                          body=self._get_request_data(body)
                                          )
        data = self._get_data(res_body, method=POST, response=resp)

        return resp, data

    def _posta(self, url='', body=None):
        post_body = None
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
                post_body = body or self.managed_object.representation
            else:
                raise URLNotSpecifiedError()
        else:
            self.url = url
            post_body = body or self.managed_object.representation
        post_body = self.remove_None_fields_from_dict(post_body)
        resp, body = self.client.post(self.url,
                                      body=self._get_request_data(post_body)
                                      )
        data = self._get_data(body, method=POSTA, response=resp)
        if not isinstance(data, list):
            raise Exception("The parsed posta response data should be a list.")
        res_list = []
        for s_data in data:
            res_data, res_url = s_data
            if self.ResponseParser.error_status_key in res_data:
                res = res_data.get(self.ResponseParser.error_status_key)
            else:
                res = self._return_new_resource_by_response_data(
                    resp,
                    res_data.get(self.ResponseParser.resource_data_key),
                    res_url
                )
            res_list.append(res)
        return resp, res_list

    def _put(self, url='', body=None):
        put_body = None
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
                put_body = body or self.managed_object.representation
            else:
                raise URLNotSpecifiedError()
        else:
            self.url = url
            put_body = body
        resp, body = self.client.put(self.url,
                                     body=self._get_request_data(put_body)
                                     )
        data = self._get_data(body, method='PUT', response=resp)
        return resp, data

    def _patch(self, url='', body=None):
        patch_body = None
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
                patch_body = body if body else \
                    self.managed_object._get_modified_info_dict()
            else:
                raise URLNotSpecifiedError()
        else:
            self.url = url
            patch_body = body
        resp, body = self.client.patch(self.url,
                                       body=self._get_request_data(patch_body)
                                       )
        data = self._get_data(body, method='PATCH', response=resp)
        return resp, data

    def _delete(self, url=''):
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
            else:
                raise URLNotSpecifiedError()
        else:
            self.url = url
        resp, body = self.client.delete(self.url)
        data = self._get_data(body, method='DELETE', response=resp)
        return resp, data


class DefaultManager(Manager):
    """
    Default resource manager.
    """
    resource_class = Resource
    resource_type = 'default'

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(resource_id=resource_id, url=url,
                         obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)

    def post(self, url='', body=None):
        return self._post(url=url, body=body)

    def posta(self, url='', body=None):
        return self._posta(url=url, body=body)

    def put(self, url='', body=None):
        return self._put(url=url, body=body)

    def patch(self, url='', body=None):
        return self._patch(url=url, body=body)

    def delete(self, url=''):
        return self._delete(url=url)
