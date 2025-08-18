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

import unittest

from pyds8k.base import DefaultManager, Resource
from pyds8k.httpclient import HTTPClient


class TestCaseWithConnect(unittest.TestCase):
    def setUp(self):
        self.client = HTTPClient(
            "https://localhost:8088/api/",  # FIXME: requests required https, not sure why
            'admin',
            'admin',
            service_type='ds8k',
            port=8088,
        )
        self.base_url = self.client.base_url
        self.resource = Resource(self.client, manager=DefaultManager(self.client))
        self.domain = self.client.domain
        # self.maxDiff = None

    def tearDown(self):
        super().tearDown()


class TestCaseWithoutConnect(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
