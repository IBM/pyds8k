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

from http import HTTPStatus

import responses
from responses import matchers

from pyds8k.resources.ds8k.v1.common.types import DS8K_HMC, DS8K_HMC_CERTIFICATE

# from pyds8k.resources.ds8k.v1.hmc.certificate import HmcCertificate
from pyds8k.test.data import (
    action_response,
    action_response_json,
    upload_hmc_certificate_cert,
)
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestHmcCertificate(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()

    @responses.activate
    def test_upload_hmc_certificate(self):
        url = f'/{DS8K_HMC}/{DS8K_HMC_CERTIFICATE}'
        uri = f'{self.domain}{self.base_url}{url}'

        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=action_response_json,
            content_type='application/json',
            match=[matchers.multipart_matcher({"file": upload_hmc_certificate_cert})],
        )
        # Way 1
        resp1 = self.system.upload_hmc_signed_certificate(upload_hmc_certificate_cert)

        assert responses.calls[-1].request.method == responses.POST
        assert resp1[0].status_code == HTTPStatus.CREATED
        assert resp1[1] == action_response

        # ???: Doesn't work because HmcCertificate doesn't have a template?
        # # Way 2
        # hmc_certificate = self.system.all(
        #     '{}.{}'.format(DS8K_HMC, DS8K_HMC_CERTIFICATE),
        #     rebuild_url=True)
        # hmc_certificate2 = hmc_certificate.create(body=cert)
        # resp2, data2 = hmc_certificate_csr2.post()
        # self.assertEqual(responses.POST, responses.calls[-1].request.method)
        # # self.assertIsInstance(data2[0], HmcCertificate)
        # self.assertEqual(resp2.status_code, HTTPStatus.CREATED)
