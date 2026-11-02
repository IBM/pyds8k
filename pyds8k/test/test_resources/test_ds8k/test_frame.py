##############################################################################
# Copyright 2026 IBM Corp.
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

import json
from http import HTTPStatus

import responses

from pyds8k.resources.ds8k.v1.common.types import DS8K_FRAME
from pyds8k.resources.ds8k.v1.frames import Frame
from pyds8k.test.data import get_response_data_by_type

from .base import TestDS8KWithConnect


class TestFrame(TestDS8KWithConnect):
    def test_id_field(self):
        info = get_response_data_by_type(DS8K_FRAME)['data'][DS8K_FRAME][0]
        frame = Frame(self.client, info=info)
        assert frame.id == 'IBM.5341-C05-B0911/R1'
        assert frame.frm_num == 'R1'
        assert frame.loc == 'U5341.C05.75B0911'
        assert frame.Frame == '1'

    def test_url_has_no_id(self):
        info = get_response_data_by_type(DS8K_FRAME)['data'][DS8K_FRAME][0]
        frame = Frame(self.client, url=f'/{DS8K_FRAME}', info=info)
        assert frame.url == f'/{DS8K_FRAME}'

    @responses.activate
    def test_get_frames_empty(self):
        body = {
            "server": {"status": "ok", "code": "", "message": ""},
            "counts": {"data_counts": 0, "total_counts": 0},
            "data": {"frames": []},
        }
        responses.get(
            self.domain + self.base_url + f'/{DS8K_FRAME}',
            body=json.dumps(body),
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        assert self.system.get_frames() == []
