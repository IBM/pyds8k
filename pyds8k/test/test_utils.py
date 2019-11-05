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

from . import base
from nose.tools import nottest
from pyds8k import utils


class TestUtils(base.TestCaseWithoutConnect):

    def test_get_subclasses(self):
        class A(object):
            pass

        class B(A):
            pass

        class C(A):
            pass

        class D(B):
            pass

        class E(C):
            pass

        self.assertIn(B, utils.get_subclasses(A))
        self.assertIn(C, utils.get_subclasses(A))
        self.assertIn(D, utils.get_subclasses(A))
        self.assertIn(E, utils.get_subclasses(A))

    def test_is_absolute_url(self):
        url1 = 'http://www.example.com/test'
        url2 = 'https://www.example.com/test'
        url3 = 'ftps://www.example.com/test'
        url4 = 'ssh://www.example.com/test'
        url5 = 'www.example.com/test'
        url6 = 'example.com/test'
        url7 = 'localhost/test'
        url8 = '/test'
        for url in (url1, url2, url3, url4, url5, url6, url7):
            self.assertTrue(utils.is_absolute_url(url))
        self.assertFalse(utils.is_absolute_url(url8))

    def test_get_request_parser_class(self):
        from pyds8k.dataParser.ds8k import RequestParser
        self.assertEqual(RequestParser, utils.get_request_parser_class('ds8k'))

    def test_get_response_parser_class(self):
        from pyds8k.dataParser.ds8k import ResponseParser
        self.assertEqual(ResponseParser,
                         utils.get_response_parser_class('ds8k'))

    # def test_get_default_service_type(self):
    #     self.assertEqual('ds8k', utils.get_default_service_type())

    @nottest
    def test_get_config_settings(self):
        settings_dict = utils.get_config_settings()
        self.assertEqual(5, len(list(settings_dict.keys())))
        self.assertIsNotNone(settings_dict.get('debug'))
        self.assertIsNotNone(settings_dict.get('log_path'))
        self.assertIsNotNone(settings_dict.get('default_service_type'))
        self.assertIsNotNone(settings_dict.get('runtime_service_type'))

    @nottest
    def test_get_config_all_items(self):
        config_dict = utils.get_config_all_items()
        self.assertEqual(5, len(list(config_dict.keys())))
        self.assertIsNotNone(config_dict.get('debug'))
        self.assertIsNotNone(config_dict.get('log_path'))
        self.assertIsNotNone(config_dict.get('default_service_type'))
        self.assertIsNotNone(config_dict.get('runtime_service_type'))

    @nottest
    def test_get_config_all(self):
        config_dict = utils.get_config_all()
        self.assertEqual(1, len(list(config_dict.keys())))
        settings_dict = config_dict.get('settings')
        self.assertIsNotNone(settings_dict)
        self.assertEqual(5, len(list(settings_dict.keys())))
        self.assertIsNotNone(settings_dict.get('debug'))
        self.assertIsNotNone(settings_dict.get('log_path'))
        self.assertIsNotNone(settings_dict.get('default_service_type'))
        self.assertIsNotNone(settings_dict.get('runtime_service_type'))


'''
class TestSetConfig(unittest.TestCase):

    RUNTIME_SERVICE_TYPE = ''

    def setUp(self):
        self.RUNTIME_SERVICE_TYPE = utils.get_runtime_service_type()

    def tearDown(self):
        utils.set_runtime_service_type(self.RUNTIME_SERVICE_TYPE)

    def test_get_runtime_service_type(self):
        self.assertEqual(
            self.RUNTIME_SERVICE_TYPE,
            utils.get_runtime_service_type()
        )

    def test_set_runtime_service_type(self):
        utils.set_runtime_service_type('test')
        self.assertEqual('test', utils.get_runtime_service_type())

    def test_get_service_type(self):
        if utils.get_runtime_service_type():
            self.assertEqual(
                self.RUNTIME_SERVICE_TYPE,
                utils.get_service_type()
            )
        else:
            self.assertEqual(
                utils.get_default_service_type(),
                utils.get_service_type()
            )
        utils.set_runtime_service_type('test')
        self.assertEqual('test', utils.get_service_type())
'''
