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
from importlib import import_module
import inspect

_PREFIX = 'ds8k.v1.'
_PATH = os.path.abspath(os.path.dirname(__file__))
RESOURCES = set([os.path.splitext(resource)[0]
                 for resource in os.listdir(_PATH)
                 if os.path.isfile(os.path.join(_PATH, resource)) and
                 not str(resource).startswith('__init__')
                 ])
RESOURCE_NAME_CLASS_MAP = {}

for re in RESOURCES:
    # re_tuple = import_module('{0}.{1}'.format(__name__, re)).RESOURCE_TUPLE

    re_tuple = \
        tuple([r[1] for r in inspect.getmembers(
            import_module('{0}.{1}'.format(__name__, re)), inspect.isclass
            ) if inspect.getmodule(r[1]).__name__ ==
            '{0}.{1}'.format(__name__, re)
        ])

    # re_tuple = tuple([r[1]
    #                  for r in inspect.getmembers(import_module(
    #                                            '{0}.{1}'.format(__name__, re)
    #                                             ), inspect.isclass)
    #                  if r[0]!='Manager' and r[0]!='Resource'])
    RESOURCE_NAME_CLASS_MAP[_PREFIX + re.lower()] = re_tuple
