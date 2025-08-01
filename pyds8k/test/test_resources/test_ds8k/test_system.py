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

from http import HTTPStatus

import pytest
import responses

from pyds8k.exceptions import OperationNotAllowed
from pyds8k.resources.ds8k.v1.common.types import DS8K_SYSTEM
from pyds8k.resources.ds8k.v1.systems import System, SystemManager
from pyds8k.test.data import (
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect

system_list_response = get_response_list_data_by_type(DS8K_SYSTEM)
system_list_response_json = get_response_list_json_by_type(DS8K_SYSTEM)


class TestSystem(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.system = System(self.client, SystemManager(self.client))

    @responses.activate
    def test_get_system(self):
        url = '/systems'
        responses.get(
            self.domain + self.base_url + url,
            body=system_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        sys = self.system.get_system()
        assert isinstance(sys, System)
        sys_data = system_list_response['data']['systems'][0]
        self._assert_equal_between_dict_and_resource(sys_data, sys)

    @responses.activate
    def test_not_allowed_operations(self):
        url = '/systems'
        responses.get(
            self.domain + self.base_url + url,
            body=system_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        sys = self.system.get_system()
        with pytest.raises(OperationNotAllowed):
            sys.put()
        with pytest.raises(OperationNotAllowed):
            sys.patch()
        with pytest.raises(OperationNotAllowed):
            sys.posta()
        with pytest.raises(OperationNotAllowed):
            sys.delete()
        with pytest.raises(OperationNotAllowed):
            sys.update()
        with pytest.raises(OperationNotAllowed) as cm:
            sys.save()
        assert System.__name__ == cm.value.resource_name
