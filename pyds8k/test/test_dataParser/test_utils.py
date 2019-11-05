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

from .. import base
from pyds8k.resources import utils


class TestUtils(base.TestCaseWithoutConnect):

    def test_update_resource_id_in_url(self):
        old_id = '1'
        new_id = '2'
        old_url_str = '/default/{}'.format(old_id)
        new_url_str = '/default/{}'.format(new_id)
        old_url_dict = {
                        'rel': 'self',
                        'href': old_url_str
                        }
        new_url_dict = {
                        'rel': 'self',
                        'href': new_url_str
                        }
        self.assertEqual(
                utils.update_resource_id_in_url(old_id, new_id, old_url_str),
                new_url_str
                         )
        self.assertEqual(
                         utils.update_resource_id_in_url(old_id, new_id,
                                                         old_url_dict, 'href'
                                                         ),
                         new_url_dict
                         )
