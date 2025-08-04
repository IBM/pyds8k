##############################################################################
# Copyright 2023 IBM Corp.
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

from importlib import import_module

from pyds8k.test.utils import get_dir_mocks, get_mocks

mocks = get_mocks(__file__)
dir_mocks = get_dir_mocks(__file__)
success_response_one = {}
success_response_all = {}

for re in mocks:
    success_response_one[re] = import_module(f'{__name__}.{re}').ONE
    success_response_all[re] = import_module(f'{__name__}.{re}').ALL
