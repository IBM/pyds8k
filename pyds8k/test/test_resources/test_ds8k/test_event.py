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

from datetime import datetime

import pytest
import responses
from responses import matchers
from tzlocal import get_localzone

from pyds8k.exceptions import InvalidArgumentError
from pyds8k.resources.ds8k.v1.common.types import DS8K_EVENT
from pyds8k.test.data import get_response_list_json_by_type

from .base import TestDS8KWithConnect

event_list_response = get_response_list_json_by_type(DS8K_EVENT)


class TestHost(TestDS8KWithConnect):
    @responses.activate
    def test_get_events_by_filter_set_severity(self):
        url = '/events'

        params = {'severity': 'warning,error'}

        responses.get(
            self.domain + self.base_url + url,
            body=event_list_response,
            content_type='application/json',
            match=[matchers.query_param_matcher(params)],
        )
        self.system.get_events_by_filter(warning=True, error=True)

    @responses.activate
    def test_get_events_by_filter_set_date_error(self):
        url = '/events'

        responses.get(
            self.domain + self.base_url + url,
            body=event_list_response,
            content_type='application/json',
        )
        with pytest.raises(InvalidArgumentError):
            self.system.get_events_by_filter(before='test')

    @responses.activate
    def test_get_events_by_filter_set_date(self):
        url = '/events'
        local_time = get_localzone()
        before = datetime(2015, 4, 1, tzinfo=local_time)
        after = datetime(2015, 1, 1, tzinfo=local_time)
        params = {
            'before': before.astimezone().strftime('%Y-%m-%dT%X%z'),
            'after': after.astimezone().strftime('%Y-%m-%dT%X%z'),
        }
        responses.get(
            self.domain + self.base_url + url,
            body=event_list_response,
            content_type='application/json',
            match=[matchers.query_param_matcher(params)],
        )
        self.system.get_events_by_filter(before=before, after=after)
