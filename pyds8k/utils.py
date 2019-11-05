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

import os
import time
import configparser
from importlib import import_module
from pyds8k.messages import GET_CONFIG_SETTINGS_IOERROR, \
    GET_CONFIG_SETTINGS_ERROR

_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE_NAME = 'config.ini'
CONFIG_FILE_PATH = os.path.join(_PATH, CONFIG_FILE_NAME)
logger = None

# HTTP STATUS CODES
HTTP200 = 200
HTTP204 = 204
HTTP404 = 404
HTTP500 = 500

# HTTP METHODS
POSTA = 'POST-to-Append'
POST = 'POST'
GET = 'GET'
PUT = 'PUT'
PATCH = 'PATCH'
DELETE = 'DELETE'


def _get_logger():
    from logging import getLogger
    from pyds8k import PYDS8K_DEFAULT_LOGGER
    global logger
    if not logger:
        logger = getLogger(PYDS8K_DEFAULT_LOGGER)
    return logger


def get_subclasses(cls):
    subclasses = cls.__subclasses__()
    for sub in list(subclasses):
        subclasses.extend(get_subclasses(sub))
    return subclasses


def get_config_settings(category="settings"):
    result_dict = dict()
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        for setting, value in config.items(category):
            result_dict[setting] = value
    except IOError as e:
        _get_logger().debug(GET_CONFIG_SETTINGS_IOERROR.format(
            CONFIG_FILE_PATH,
            str(e)
            )
        )
    except Exception as e:
        _get_logger().error(GET_CONFIG_SETTINGS_ERROR.format(str(e)))
    return result_dict


def get_config_all():
    result_dict = dict()
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        for section in config.sections():
            result_dict[section] = dict()
            for setting, value in config.items(section):
                result_dict[section][setting] = value
    except IOError as e:
        _get_logger().debug(GET_CONFIG_SETTINGS_IOERROR.format(
            CONFIG_FILE_PATH,
            str(e)
            )
        )
    except Exception as e:
        _get_logger().error(GET_CONFIG_SETTINGS_ERROR.format(str(e)))
    return result_dict


def get_config_all_items():
    result_dict = dict()
    try:
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        for section in config.sections():
            for setting, value in config.items(section):
                result_dict[setting] = value
    except IOError as e:
        _get_logger().debug(GET_CONFIG_SETTINGS_IOERROR.format(
            CONFIG_FILE_PATH,
            str(e)
            )
        )
    except Exception as e:
        _get_logger().error(GET_CONFIG_SETTINGS_ERROR.format(str(e)))
    return result_dict


def get_config_by_name(name):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config.get('settings', name)


def set_config_by_name(name, value):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    config.set('settings', name, value)

    with open(CONFIG_FILE_PATH, 'wb') as config_file:
        config.write(config_file)


"""
def get_default_service_type():
    return get_config_by_name('default_service_type')


def get_default_service_version():
    return get_config_by_name('default_service_version')


def get_runtime_service_type():
    return get_config_by_name('runtime_service_type')


def get_service_type():
    return get_runtime_service_type() or get_default_service_type()


def set_runtime_service_type(service_type):
    set_config_by_name('runtime_service_type', service_type)
"""


def get_request_parser_class(service_type):
    prefix = service_type
    Parser = import_module('{0}.dataParser.{1}'.format(__package__, prefix)
                           )
    return Parser.RequestParser


def get_response_parser_class(service_type):
    prefix = service_type
    Parser = import_module('{0}.dataParser.{1}'.format(__package__, prefix)
                           )
    return Parser.ResponseParser


def timer(func):
    def inner(self, *args, **kwargs):
        start = time.time()
        result = func(self, *args, **kwargs)
        end = time.time()
        _get_logger().info(
            "Successfully called method '{}' in {} seconds".format(
                func.__name__,
                round(end - start, 2)
            )
        )
        return result
    return inner


def res_timer_recorder(func):
    def inner(self, *args, **kwargs):
        start = time.time()
        res = func(self, *args, **kwargs)
        end = time.time()
        sec = round(end - start, 2)
        if not res:
            _get_logger().info(
                "Successfully got 0 resources in {} seconds".format(sec)
            )
            return []
        _get_logger().info(
            "Successfully got {} resources in {} seconds, \
{} seconds per 100 instances.".format(
                len(res),
                sec,
                round(sec / len(res) * 100, 2)
            )
        )
        return res
    return inner


def dictionarize(func):
    def inner(self, *args, **kwargs):
        res_obj = func(self, *args, **kwargs)
        if not isinstance(res_obj, list):
            res_obj = [res_obj, ]
        coverted = []
        for res in res_obj:
            coverted.append(res.representation)
        return coverted
    return inner


def is_absolute_url(url):
    if url.startswith('/'):
        return False
    elif '//' in url:
        return True
    # Don't verify the URI's validation here.
    else:
        return True
