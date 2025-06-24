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

import pytest

from pyds8k import utils
from pyds8k.dataParser.ds8k import RequestParser, ResponseParser

from . import base

NUM_CONFIG_DICT_KEYS = 5


class TestUtils(base.TestCaseWithoutConnect):
    def test_get_subclasses(self):
        class A:
            pass

        class B(A):
            pass

        class C(A):
            pass

        class D(B):
            pass

        class E(C):
            pass

        assert B in utils.get_subclasses(A)
        assert C in utils.get_subclasses(A)
        assert D in utils.get_subclasses(A)
        assert E in utils.get_subclasses(A)

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
            assert utils.is_absolute_url(url)
        assert not utils.is_absolute_url(url8)

    def test_get_request_parser_class(self):
        assert RequestParser == utils.get_request_parser_class('ds8k')

    def test_get_response_parser_class(self):
        assert ResponseParser == utils.get_response_parser_class('ds8k')

    # def test_get_default_service_type(self):
    #     self.assertEqual('ds8k', utils.get_default_service_type())

    @pytest.mark.skip
    def test_get_config_settings(self):
        settings_dict = utils.get_config_settings()
        assert len(list(settings_dict.keys())) == NUM_CONFIG_DICT_KEYS
        assert settings_dict.get('debug') is not None
        assert settings_dict.get('log_path') is not None
        assert settings_dict.get('default_service_type') is not None
        assert settings_dict.get('runtime_service_type') is not None

    @pytest.mark.skip
    def test_get_config_all_items(self):
        config_dict = utils.get_config_all_items()
        assert len(list(config_dict.keys())) == NUM_CONFIG_DICT_KEYS
        assert config_dict.get('debug') is not None
        assert config_dict.get('log_path') is not None
        assert config_dict.get('default_service_type') is not None
        assert config_dict.get('runtime_service_type') is not None

    @pytest.mark.skip
    def test_get_config_all(self):
        config_dict = utils.get_config_all()
        assert len(list(config_dict.keys())) == 1
        settings_dict = config_dict.get('settings')
        assert settings_dict is not None
        assert len(list(settings_dict.keys())) == NUM_CONFIG_DICT_KEYS
        assert settings_dict.get('debug') is not None
        assert settings_dict.get('log_path') is not None
        assert settings_dict.get('default_service_type') is not None
        assert settings_dict.get('runtime_service_type') is not None


'''
class TestSetConfig(unittest.TestCase):

    RUNTIME_SERVICE_TYPE = ''

    def setUp(self):
        self.RUNTIME_SERVICE_TYPE = utils.get_runtime_service_type()

    def tearDown(self):
        utils.set_runtime_service_type(self.RUNTIME_SERVICE_TYPE)

    def test_get_runtime_service_type(self):
        assert utils.get_runtime_service_type() == self.RUNTIME_SERVICE_TYPE

    def test_set_runtime_service_type(self):
        utils.set_runtime_service_type('test')
        assert utils.get_runtime_service_type() == 'test'

    def test_get_service_type(self):
        if utils.get_runtime_service_type():
            assert utils.get_service_type() == self.RUNTIME_SERVICE_TYPE
        else:
            assert utils.get_default_service_type() == utils.get_service_type()
        utils.set_runtime_service_type('test')
        assert utils.get_service_type() == 'test'
'''
