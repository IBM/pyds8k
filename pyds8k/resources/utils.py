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

from pyds8k.exceptions import URLParseError
from pyds8k import PYDS8K_DEFAULT_LOGGER
from logging import getLogger

logger = getLogger(PYDS8K_DEFAULT_LOGGER)


def update_resource_id_in_url(old_id, new_id, url, field=''):
    if not field:
        if not isinstance(url, str):
            raise URLParseError()
        else:
            return url.replace(old_id, new_id, 1)
    else:
        try:
            url[field] = str(url[field]).replace(old_id, new_id, 1)
        except Exception:
            raise URLParseError()
        return url
