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
from pyds8k.httpclient import HTTPClient
from pyds8k.base import Resource, DefaultManager


class TestCaseWithConnect(unittest.TestCase):

    def setUp(self):
        self.client = HTTPClient(service_address='localhost',
                                 user='admin',
                                 password='admin',
                                 service_type='ds8k',
                                 port='8088')
        self.resource = Resource(self.client, DefaultManager(self.client))
        self.domain = self.client.domain
        # self.maxDiff = None

    def tearDown(self):
        super(TestCaseWithConnect, self).tearDown()


class TestCaseWithoutConnect(unittest.TestCase):

    def setUp(self):
        super(TestCaseWithoutConnect, self).setUp()

    def tearDown(self):
        super(TestCaseWithoutConnect, self).tearDown()
