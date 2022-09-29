import json

import httpretty

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_CS_FLASHCOPY, \
    DS8K_COPY_SERVICE_PREFIX, DS8K_FLASHCOPY
from pyds8k.resources.ds8k.v1.cs.flashcopies import FlashCopy as FlashCopies
from pyds8k.resources.ds8k.v1.flashcopy import FlashCopy
from pyds8k.test.data import get_response_json_by_type, \
    get_response_data_by_type, action_response_json, \
    create_flashcopy_response_json
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestFlashCopies(TestDS8KWithConnect):

    def setUp(self):
        super(TestFlashCopies, self).setUp()
        self.maxDiff = None

    @httpretty.activate
    def test_create_cs_flashcopy(self):
        url = '/cs/flashcopies'

        source_volume = '0000'
        target_volume = '0001'

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            req = RequestParser(
                {"volume_pairs": [{"source_volume": source_volume,
                                   "target_volume": target_volume
                                   }],
                 "options": []
                 })
            assert {
                    **json.loads(request.body).get('request').get('params'),
                    **req.get_request_data().get('request').get('params')
                    } == json.loads(request.body).get('request').get('params')
            return (201, headers, create_flashcopy_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        # Way 1
        resp1 = self.system.create_cs_flashcopy(
            volume_pairs=[{'source_volume': source_volume,
                           'target_volume': target_volume}])
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(resp1[0], FlashCopies)

        # Way 2
        flashcopies = self.system.all(
            '{}.{}'.format(DS8K_COPY_SERVICE_PREFIX, DS8K_CS_FLASHCOPY),
            rebuild_url=True)
        new_fc2 = flashcopies.create(volume_pairs=[
            {'source_volume': source_volume, 'target_volume': target_volume}])
        resp2, data2 = new_fc2.posta()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data2[0], FlashCopies)
        self.assertEqual(resp2.status_code, 201)

        # Way 3
        flashcopies = self.system.all(
            '{}.{}'.format(DS8K_COPY_SERVICE_PREFIX, DS8K_CS_FLASHCOPY),
            rebuild_url=True)
        new_fc3 = flashcopies.create(volume_pairs=[
            {'source_volume': source_volume, 'target_volume': target_volume}])
        resp3, data3 = new_fc3.save()
        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIsInstance(data3[0], FlashCopies)
        self.assertEqual(resp3.status_code, 201)

    @httpretty.activate
    def test_delete_cs_flashcopy(self):
        response_a_json = get_response_json_by_type(DS8K_CS_FLASHCOPY)
        response_a = get_response_data_by_type(DS8K_CS_FLASHCOPY)
        name = self._get_resource_id_from_resopnse(DS8K_FLASHCOPY,
                                                   response_a,
                                                   FlashCopy.id_field
                                                   )
        url = '/cs/flashcopies/{}'.format(name)
        httpretty.register_uri(httpretty.GET,
                               self.domain + self.base_url + url,
                               body=response_a_json,
                               content_type='application/json',
                               status=200,
                               )
        httpretty.register_uri(httpretty.DELETE,
                               self.domain + self.base_url + url,
                               body=action_response_json,
                               content_type='application/json',
                               status=204,
                               )
        # Way 1
        _ = self.system.delete_cs_flashcopy(name)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)

        # Way 2
        flashcopy = self.system.get_cs_flashcopies(name)
        self.assertIsInstance(flashcopy, FlashCopies)
        resp2, _ = flashcopy.delete()
        self.assertEqual(resp2.status_code, 204)
        self.assertEqual(httpretty.DELETE, httpretty.last_request().method)
