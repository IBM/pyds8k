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

"""
DS8K resources base interface.
"""

import contextlib
from logging import getLogger

from pyds8k import PYDS8K_DEFAULT_LOGGER
from pyds8k.base import Manager, Resource, get_resource_and_manager_class_by_route
from pyds8k.exceptions import FieldReadOnly, OperationNotAllowed, URLNotSpecifiedError
from pyds8k.messages import INVALID_TYPE

from .mixins import RootResourceMixin

logger = getLogger(PYDS8K_DEFAULT_LOGGER)


class Base(RootResourceMixin, Resource):
    # If there is a field named "id" in response data,
    # the id_field can't be set to value other than "id"
    id_field = 'id'
    url_field = 'link'
    base_url = ''
    create_method = 'posta'
    # Required only in writable resources, fileds are from _template
    # Resource id is exclude.
    readonly_fileds = ()
    # Not like related_resource, related_resources_list is not set during
    # loading, its keys use lazy-loading to get details.
    related_resources_collection = ()

    def _add_details(self, info, force=False):
        super()._add_details(info, force=force)
        self._start_updating()
        self._set_related_resources_collection()
        self._stop_updating()

    def _set_related_resources_collection(self):
        for key in self.related_resources_collection:
            res = self.representation.get(key)
            # If the related resources(should be a list) are not in info,
            # will empty them and wait for lazy-loading.
            if not isinstance(res, list):
                self.representation[key] = ''
                with contextlib.suppress(AttributeError):
                    delattr(self, key)
            # If the related resources(should be a list) are in info, set it.
            else:
                re_class, re_manager = self._get_resource_class_by_name(key)
                res_list = [
                    re_class(self.client, manager=re_manager(self.client), info=r)
                    for r in res
                ]
                setattr(self, key, res_list)

    def __setattr__(self, key, value):
        if key in self.readonly_fileds and not self.is_updating():
            raise FieldReadOnly(key)
        super().__setattr__(key, value)
        try:
            if key in self.related_resources_collection:
                ids = [getattr(item, item.id_field) for item in value]
                self.representation[key] = ids
                if not self.is_updating():
                    self._set_modified_info_dict(key, ids)
        except AttributeError:
            pass

    def __getattr__(self, key):
        if key in self.related_resources_collection:
            try:
                return getattr(self, f'get_{key}')()
            except Exception as exc:
                logger.debug(f"Can not get {key} from {self}, reason is: {type(exc)}")
                raise AttributeError(key) from exc
        return super().__getattr__(key)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._get_id()}>"

    def _get_resource_class_by_name(self, resource_type):
        prefix = f'{self.client.service_type}.{self.client.service_version}'
        return get_resource_and_manager_class_by_route(f"{prefix}.{resource_type}")

    def _verify_type(self, new_type, valid_type_list):
        if new_type and new_type not in valid_type_list:
            raise ValueError(INVALID_TYPE.format(', '.join(valid_type_list)))


class SingletonBase(Base):
    # A singleton resource has no id field by default
    id_field = '*'


class BaseManager(Manager):
    resource_class = Base
    response_key = 'data'
    resource_type = ''

    def _post(self, url='', body=None):
        post_body = None
        if not body:
            if self.managed_object is not None:
                post_body = self.managed_object._get_modified_info_dict()
                # repre = self.managed_object.representation
                # post_body = {key: value
                #             for key, value in repre.iteritems()
                #             if key not in self.managed_object.readonly_fileds
                #             }
            else:
                raise URLNotSpecifiedError
        else:
            post_body = body
        return super()._post(url=url, body=post_body)

    # DS8K will use PUT in PATCH way, and don't use PATCH.
    def _put(self, url='', body=None):
        put_body = None
        if not url:
            if self.managed_object is not None:
                self.url = self.managed_object.url
                # use modified info here
                put_body = (
                    body if body else self.managed_object._get_modified_info_dict()
                )
            else:
                raise URLNotSpecifiedError
        else:
            self.url = url
            put_body = body
        resp, body = self.client.put(self.url, body=self._get_request_data(put_body))
        data = self._get_data(body, method='PUT', response=resp)
        return resp, data

    def _patch(self, url='', body=None):
        return self._put(url=url, body=body)

    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        msg = 'get'
        raise OperationNotAllowed(msg, self.resource_class.__name__)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        msg = 'list'
        raise OperationNotAllowed(msg, self.resource_class.__name__)

    def post(self, url='', body=None):
        msg = 'post'
        raise OperationNotAllowed(msg, self.resource_class.__name__)

    def posta(self, url='', body=None):
        msg = 'posta'
        raise OperationNotAllowed(msg, self.resource_class.__name__)

    def put(self, url='', body=None):
        msg = 'put'
        raise OperationNotAllowed(msg, self.resource_class.__name__)

    def patch(self, url='', body=None):
        msg = 'patch'
        raise OperationNotAllowed(msg, self.resource_class.__name__)

    def delete(self, url=''):
        msg = 'delete'
        raise OperationNotAllowed(msg, self.resource_class.__name__)


class ReadOnlyManager(BaseManager):
    def get(self, resource_id='', url='', obj_class=None, **kwargs):
        return self._get(
            resource_id=resource_id, url=url, obj_class=obj_class, **kwargs
        )

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)


class SingletonBaseManager(BaseManager):
    def get(self, url='', obj_class=None, **kwargs):
        return self._get(url=url, obj_class=obj_class, **kwargs)

    def list(self, url='', obj_class=None, body=None, **kwargs):
        return self._list(url=url, obj_class=obj_class, body=body, **kwargs)
