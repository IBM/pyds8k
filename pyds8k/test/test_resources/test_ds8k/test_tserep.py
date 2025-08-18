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

from http import HTTPStatus

import responses
from responses import matchers

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_TSEREP
from pyds8k.resources.ds8k.v1.pools import Pool
from pyds8k.resources.ds8k.v1.tserep import TSERep
from pyds8k.test.data import (
    action_response_json,
    get_response_list_data_by_type,
    get_response_list_json_by_type,
)

from .base import TestDS8KWithConnect

tserep_list_response_json = get_response_list_json_by_type(DS8K_TSEREP)


class TestTSERep(TestDS8KWithConnect):
    def test_pool_field(self):
        tserep = get_response_list_data_by_type(DS8K_TSEREP)['data'][DS8K_TSEREP][0]
        pool_id = tserep['pool'][Pool.id_field]
        tse = TSERep(self.client, info=tserep)
        assert tse.pool == pool_id
        assert tse.representation['pool'] == pool_id
        assert isinstance(tse._pool, Pool)
        assert tse._pool.id == pool_id

    @responses.activate
    def test_update(self):
        pool_id = 'P1'
        url = f'/pools/{pool_id}/tserep'
        uri = f'{self.domain}{self.base_url}{url}'

        cap = '10'
        threshold = '70'

        responses.get(
            uri,
            body=tserep_list_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        resq = RequestParser({'cap': cap, 'threshold': threshold})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )
        tserep = self.system.get_tserep_by_pool(pool_id)

        tserep.cap = cap
        tserep.threshold = threshold
        tserep.save()
