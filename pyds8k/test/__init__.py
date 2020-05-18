import os
from importlib import import_module

_PATH = os.path.abspath(os.path.dirname(__file__))
mocks = set([os.path.splitext(resource)[0]
             for resource in os.listdir(_PATH)
             if os.path.isfile(os.path.join(_PATH, resource)) and
             not str(resource).startswith('__init__')
             ])
dir_mocks = \
    [resource for resource in os.listdir(_PATH) if os.path.isdir(
        os.path.join(_PATH, resource)
        )]
success_response_one = {}
success_response_all = {}

for re in mocks:
    success_response_one[re] = import_module(
        '{0}.{1}'.format(__name__, re)
    ).ONE
    success_response_all[re] = import_module(
        '{0}.{1}'.format(__name__, re)
    ).ALL