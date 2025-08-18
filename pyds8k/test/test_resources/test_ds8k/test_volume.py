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

import json
from http import HTTPStatus

import pytest
import responses
from responses import matchers

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.exceptions import FieldReadOnly
from pyds8k.messages import INVALID_TYPE
from pyds8k.resources.ds8k.v1.common import types
from pyds8k.resources.ds8k.v1.common.types import DS8K_VOLUME
from pyds8k.resources.ds8k.v1.flashcopy import FlashCopy
from pyds8k.resources.ds8k.v1.hosts import Host
from pyds8k.resources.ds8k.v1.lss import LSS
from pyds8k.resources.ds8k.v1.pools import Pool
from pyds8k.resources.ds8k.v1.pprc import PPRC
from pyds8k.resources.ds8k.v1.volumes import Volume, VolumeManager
from pyds8k.test.data import (
    action_response,
    action_response_json,
    create_volume_response,
    create_volume_response_json,
    create_volumes_partial_failed_response,
    create_volumes_partial_failed_response_json,
    create_volumes_response_json,
    get_response_data_by_type,
    get_response_json_by_type,
)
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestVolume(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()
        self.volume = Volume(self.client, VolumeManager(self.client))
        self.maxDiff = None

    def test_invalid_volume_type(self):
        with pytest.raises(
            ValueError, match=INVALID_TYPE.format(', '.join(types.DS8K_VOLUME_TYPES))
        ):
            Volume(self.client, volume_type='fake')

    def test_related_resource_field(self):
        volume_info = get_response_data_by_type(DS8K_VOLUME)['data'][DS8K_VOLUME][0]
        pool_id = volume_info['pool'][Pool.id_field]
        lss_id = volume_info['lss']['id']
        volume = Volume(self.client, info=volume_info)
        assert volume.pool == pool_id
        assert volume.representation['pool'] == pool_id
        assert isinstance(volume._pool, Pool)
        assert volume._pool.id == pool_id
        assert volume.lss == lss_id
        assert volume.representation['lss'] == lss_id
        assert isinstance(volume._lss, LSS)
        assert volume._lss.id == lss_id

        volume.pool = 'new_pool'
        assert volume.pool == 'new_pool'
        assert volume.representation['pool'] == 'new_pool'

        with pytest.raises(FieldReadOnly):
            volume.lss = 'new_lss'

    def test_related_resources_collection(self):
        hosts = [Host(self.client, resource_id=f'host{i}') for i in range(10)]

        flashcopies = [FlashCopy(self.client, resource_id=f'fc{i}') for i in range(10)]

        pprc = [PPRC(self.client, resource_id=f'pprc{i}') for i in range(10)]

        # init without related_resources collection
        volume = Volume(
            self.client,
            info={
                'name': 'a_0000',
                'link': {'rel': 'self', 'href': '/api/volumes/a_0000'},
                'hosts': {
                    'link': {'rel': 'self', 'href': '/api/hosts'},
                },
            },
        )
        for i in volume.related_resources_collection:
            assert volume.representation.get(i) == ''
            assert not hasattr(volume, i)

        # loading related resources collection
        volume._start_updating()
        setattr(volume, types.DS8K_HOST, hosts)
        setattr(volume, types.DS8K_FLASHCOPY, flashcopies)
        setattr(volume, types.DS8K_PPRC, pprc)
        volume._stop_updating()
        for j, value in enumerate(volume.representation[types.DS8K_HOST]):
            assert value == getattr(hosts[j], hosts[j].id_field)
        for k, value in enumerate(volume.representation[types.DS8K_FLASHCOPY]):
            assert value == getattr(flashcopies[k], flashcopies[k].id_field)
        for vol, value in enumerate(volume.representation[types.DS8K_PPRC]):
            assert value == getattr(pprc[vol], pprc[vol].id_field)

    @responses.activate
    def test_delete_volume(self):
        response_a_json = get_response_json_by_type(DS8K_VOLUME)
        response_a = get_response_data_by_type(DS8K_VOLUME)
        name = self._get_resource_id_from_resopnse(
            DS8K_VOLUME, response_a, Volume.id_field
        )
        url = f'/volumes/{name}'
        responses.get(
            self.domain + self.base_url + url,
            body=response_a_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )
        responses.delete(
            self.domain + self.base_url + url,
            body=action_response_json,
            content_type='application/json',
            status=HTTPStatus.OK.value,
        )

        # Way 1
        _ = self.system.delete_volume(name)
        assert responses.calls[-1].request.method == responses.DELETE
        # self.assertEqual(resp1, action_response['server'])

        # Way 2
        volume = self.system.get_volume(name)
        assert isinstance(volume, Volume)
        resp2, _ = volume.delete()
        assert resp2.status_code == HTTPStatus.OK.value
        assert responses.calls[-1].request.method == responses.DELETE

    @responses.activate
    def test_update_volume_rename(self):
        volume_id = 'a_0000'
        url = f'/volumes/{volume_id}'
        uri = f'{self.domain}{self.base_url}{url}'

        new_name = 'new_name'

        resq = RequestParser({'name': new_name})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        res = self.system.update_volume_rename(volume_id, new_name)
        assert responses.calls[-1].request.method == responses.PUT
        assert res == action_response['server']

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.name = new_name
        _, body = vol.save()
        assert responses.calls[-1].request.method == responses.PUT
        assert body == action_response['server']

    @responses.activate
    def test_update_volume_extend(self):
        volume_id = 'a_0000'
        url = f'/volumes/{volume_id}'
        uri = f'{self.domain}{self.base_url}{url}'

        new_size = '100'
        captype = 'gib'

        resq = RequestParser({'cap': new_size, 'captype': captype})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        res = self.system.update_volume_extend(volume_id, new_size, captype)
        assert responses.calls[-1].request.method == responses.PUT
        assert res == action_response['server']

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.cap = new_size
        vol.captype = captype
        _, body = vol.save()
        assert responses.calls[-1].request.method == responses.PUT
        assert body == action_response['server']

    @responses.activate
    def test_update_volume_move(self):
        volume_id = 'a_0000'
        url = f'/volumes/{volume_id}'
        uri = f'{self.domain}{self.base_url}{url}'

        new_pool = 'new_pool'

        resq = RequestParser({'pool': new_pool})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        res = self.system.update_volume_move(volume_id, new_pool)
        assert responses.calls[-1].request.method == responses.PUT
        assert res == action_response['server']

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.pool = new_pool
        _, body = vol.save()
        assert responses.calls[-1].request.method == responses.PUT
        assert body == action_response['server']

    @pytest.mark.skip
    @responses.activate
    def test_update_volume_map(self):
        volume_id = 'a_0000'
        url = f'/volumes/{volume_id}'
        uri = f'{self.domain}{self.base_url}{url}'

        host_name = 'host1'

        resq = RequestParser({'host': host_name})
        responses.put(
            uri,
            status=HTTPStatus.OK,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        res = self.system.update_volume_map(volume_id, host_name)
        assert responses.calls[-1].method == responses.PUT
        assert res == action_response['server']

        vol = self.system.one(DS8K_VOLUME, volume_id, rebuild_url=True)
        vol._add_details({'name': volume_id})
        vol.host = host_name

    @responses.activate
    def test_create_volume(self):
        url = '/volumes'
        uri = f'{self.domain}{self.base_url}{url}'

        name = 'volume1'
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'

        req = RequestParser(
            {
                'name': name,
                'cap': cap,
                'captype': captype,
                'stgtype': stgtype,
                'pool': pool,
                'lss': lss,
                'tp': tp,
            }
        )
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=create_volume_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        # Way 1
        resp1 = self.system.create_volume(
            name=name,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], Volume)

        # Way 2
        volume = self.system.all(DS8K_VOLUME, rebuild_url=True)
        new_vol2 = volume.create(
            name=name,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
        )
        resp2, data2 = new_vol2.posta()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data2[0], Volume)
        assert resp2.status_code == HTTPStatus.CREATED

        # Way 3
        volume = self.system.all(DS8K_VOLUME, rebuild_url=True)
        new_vol3 = volume.create(
            name=name,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
        )
        resp3, data3 = new_vol3.save()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data3[0], Volume)
        assert resp3.status_code == HTTPStatus.CREATED

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.

    @responses.activate
    def test_create_volumes(self):
        url = '/volumes'
        uri = f'{self.domain}{self.base_url}{url}'

        name = 'volume1'
        quantity = '10'
        namecol = [f'volume{i}' for i in range(10)]
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'

        resq = RequestParser(
            {
                'name': name,
                'cap': cap,
                'pool': pool,
                'stgtype': stgtype,
                'captype': captype,
                'lss': lss,
                'tp': tp,
                'quantity': quantity,
            }
        )
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=create_volumes_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        resq = RequestParser(
            {
                'namecol': namecol,
                'cap': cap,
                'captype': captype,
                'stgtype': stgtype,
                'pool': pool,
                'lss': lss,
                'tp': tp,
            }
        )
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=create_volumes_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        resp1 = self.system.create_volumes_with_same_prefix(
            name,
            cap,
            pool,
            quantity=quantity,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], Volume)

        resp2 = self.system.create_volumes_without_same_prefix(
            namecol, cap, pool, stgtype=stgtype, captype=captype, lss=lss, tp=tp
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp2[0], Volume)

        resp3 = self.system.create_volumes_with_names(
            namecol, cap, pool, stgtype=stgtype, captype=captype, lss=lss, tp=tp
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp3[0], Volume)

    @responses.activate
    def test_create_volumes_partial_failed(self):
        url = '/volumes'
        uri = f'{self.domain}{self.base_url}{url}'

        name = 'volume1'
        quantity = '10'
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'

        resq = RequestParser(
            {
                'name': name,
                'cap': cap,
                'pool': pool,
                'stgtype': stgtype,
                'captype': captype,
                'lss': lss,
                'tp': tp,
                'quantity': quantity,
            }
        )
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=create_volumes_partial_failed_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(resq.get_request_data())],
        )

        resp1 = self.system.create_volumes_with_same_prefix(
            name,
            cap,
            pool,
            quantity=quantity,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
        )
        assert responses.calls[-1].request.method == responses.POST
        # return 1 created volume and 1 error status
        assert isinstance(resp1[0], Volume)
        assert isinstance(resp1[1], dict)
        assert resp1[1] == create_volumes_partial_failed_response.get('responses')[
            1
        ].get('server')

    def test_create_volume_type_error(self):
        with pytest.raises(
            ValueError, match=INVALID_TYPE.format(', '.join(types.DS8K_VOLUME_TYPES))
        ):
            self.system.create_volume('name', '10', 'testpool_0', 'fake_stgtype')
        with pytest.raises(
            ValueError, match=INVALID_TYPE.format(', '.join(types.DS8K_CAPTYPES))
        ):
            self.system.create_volume(
                'name',
                '10',
                'testpool_0',
                types.DS8K_VOLUME_TYPE_FB,
                captype='fake_captype',
            )
        with pytest.raises(
            ValueError, match=INVALID_TYPE.format(', '.join(types.DS8K_TPS))
        ):
            self.system.create_volume(
                'name', '10', 'testpool_0', types.DS8K_VOLUME_TYPE_FB, tp='fake_tp'
            )

    @responses.activate
    def test_create_volume_with_volid(self):
        url = '/volumes'
        uri = f'{self.domain}{self.base_url}{url}'

        name = 'volume1'
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'
        _id = '0000'

        req = RequestParser(
            {
                'name': name,
                'cap': cap,
                'pool': pool,
                'stgtype': stgtype,
                'captype': captype,
                'lss': lss,
                'tp': tp,
                'id': _id,
            }
        )

        prepared_response = create_volume_response.copy()
        prepared_response['data']['volumes'][0]['id'] = _id
        prepared_href = f"{self.domain}{self.base_url}{url}/{_id}"
        prepared_response['link']['href'] = prepared_href
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=json.dumps(prepared_response),
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        # Way 1
        resp1 = self.system.create_volume(
            name=name,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            id=_id,
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], Volume)

        # Way 2
        volume = self.system.all(DS8K_VOLUME, rebuild_url=True)
        new_vol2 = volume.create(
            name=name,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            id=_id,
        )
        resp2, data2 = new_vol2.posta()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data2[0], Volume)
        assert resp2.status_code == HTTPStatus.CREATED

        # Way 3
        volume = self.system.all(DS8K_VOLUME, rebuild_url=True)
        new_vol3 = volume.create(
            name=name,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            id=_id,
        )
        resp3, data3 = new_vol3.save()
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(data3[0], Volume)
        assert resp3.status_code == HTTPStatus.CREATED

        # Way 4
        # Don't init a resource instance by yourself when create new.
        # use .create() instead.

    @responses.activate
    def test_create_volumes_with_volids(self):
        url = '/volumes'
        uri = f'{self.domain}{self.base_url}{url}'

        name_col = ['volume0000']
        cap = '10'
        pool = 'testpool_0'
        stgtype = types.DS8K_VOLUME_TYPE_FB
        captype = 'gib'
        tp = 'ese'
        lss = '00'
        ids = ['0000']

        req = RequestParser(
            {
                'name_col': name_col,
                'cap': cap,
                'captype': captype,
                'stgtype': stgtype,
                'pool': pool,
                'lss': lss,
                'tp': tp,
                'ids': ids,
            }
        )

        # CAVEAT: The REST api uses namecol, not name_col.
        prepared_request = req.get_request_data()
        prepared_request['request']['params']['namecol'] = prepared_request['request'][
            'params'
        ]['name_col']
        del prepared_request['request']['params']['name_col']

        prepared_response = create_volume_response.copy()
        prepared_response['data']['volumes'][0]['id'] = ids[0]
        prepared_href = f"{self.domain}{self.base_url}{url}/{ids[0]}"
        prepared_response['link']['href'] = prepared_href

        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=json.dumps(prepared_response),
            content_type='application/json',
            match=[matchers.json_params_matcher(prepared_request)],
        )

        resp1 = self.system.create_volumes(
            name_col=name_col,
            cap=cap,
            pool=pool,
            stgtype=stgtype,
            captype=captype,
            lss=lss,
            tp=tp,
            ids=ids,
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], Volume)

    @responses.activate
    def test_create_alias_volumes(self):
        url = '/volumes'
        uri = f'{self.domain}{self.base_url}{url}'

        vol_id = '00FF'
        quantity = 2
        alias_create_order = 'decrement'
        ckd_base_ids = ['0000', '0001']

        req = RequestParser(
            {
                'id': vol_id,
                'quantity': quantity,
                'alias': 'true',  # CAVEAT: The API always sends true.
                'alias_create_order': alias_create_order,
                'ckd_base_ids': ckd_base_ids,
            }
        )

        prepared_response = create_volume_response.copy()
        prepared_response['data']['volumes'][0]['id'] = vol_id
        prepared_href = f"{self.domain}{self.base_url}{url}/{vol_id}"
        prepared_response['link']['href'] = prepared_href

        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=json.dumps(prepared_response),
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        resp1 = self.system.create_alias_volumes(
            vol_id, ckd_base_ids, quantity=quantity
        )
        assert responses.calls[-1].request.method == responses.POST
        assert isinstance(resp1[0], Volume)
