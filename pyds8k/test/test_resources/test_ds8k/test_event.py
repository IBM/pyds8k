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
from datetime import datetime
from .base import TestDS8KWithConnect
from ...data import get_response_list_json_by_type
from pyds8k.resources.ds8k.v1.common.types import DS8K_EVENT
from pyds8k.exceptions import InvalidArgumentError

event_list_response = get_response_list_json_by_type(DS8K_EVENT)


class TestHost(TestDS8KWithConnect):

    @httpretty.activate
    def test_get_events_by_filter_set_severity(self):
        url = '/events'

        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=event_list_response,
                               content_type='application/json',
                               )
        self.system.get_events_by_filter(warning=True, error=True)
        req = httpretty.last_request()
        self.assertIsNotNone(req.querystring)
        self.assertIn('severity', req.querystring)
        self.assertEqual('warning,error', req.querystring.get('severity')[0])

    @httpretty.activate
    def test_get_events_by_filter_set_date_error(self):
        url = '/events'

        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=event_list_response,
                               content_type='application/json',
                               )
        with self.assertRaises(InvalidArgumentError):
            self.system.get_events_by_filter(before='test')

    @httpretty.activate
    def test_get_events_by_filter_set_date(self):
        url = '/events'
        before = datetime(2015, 4, 1)
        after = datetime(2015, 1, 1)

        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=event_list_response,
                               content_type='application/json',
                               )
        self.system.get_events_by_filter(before=before, after=after)
        req = httpretty.last_request()
        self.assertIsNotNone(req.querystring)
        self.assertIn('before', req.querystring)
        self.assertIn('after', req.querystring)

        # httpretty unquote "+" and " " in a wrong way,
        # so I can not verify time zone here.
        self.assertEqual('2015-04-01T00:00:00',
                         req.querystring.get('before')[0][:-5]
                         )
        self.assertEqual('2015-01-01T00:00:00',
                         req.querystring.get('after')[0][:-5]
                         )
