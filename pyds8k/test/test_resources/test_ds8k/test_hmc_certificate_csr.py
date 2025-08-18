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

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import (
    DS8K_HMC,
    DS8K_HMC_CERTIFICATE,
    DS8K_HMC_CERTIFICATE_CSR,
)

# from pyds8k.resources.ds8k.v1.hmc.certificate.csr import HmcCertificateCsr
from pyds8k.test.data import create_hmc_certificate_csr_response_json
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestHmcCertificateCsr(TestDS8KWithConnect):
    def setUp(self):
        super().setUp()

    @responses.activate
    def test_create_hmc_certificate_csr(self):
        url = f'/{DS8K_HMC}/{DS8K_HMC_CERTIFICATE}/{DS8K_HMC_CERTIFICATE_CSR}'
        uri = f'{self.domain}{self.base_url}{url}'

        O = "IBM"  # noqa: E741, N806
        OU = "DS8000"  # noqa: N806
        C = "US"  # noqa: N806
        ST = "NY"  # noqa: N806
        L = "Armok"  # noqa: N806
        email = "ansible@fake_server.com"
        force = "True"

        req = RequestParser(
            {
                'O': O,
                'OU': OU,
                'C': C,
                'ST': ST,
                'L': L,
                'email': email,
                'force': force,
            }
        )
        responses.post(
            uri,
            status=HTTPStatus.CREATED,
            body=create_hmc_certificate_csr_response_json,
            content_type='application/json',
            match=[matchers.json_params_matcher(req.get_request_data())],
        )

        # Way 1
        resp1 = self.system.create_hmc_csr(
            O=O, OU=OU, C=C, ST=ST, L=L, email=email, force=force
        )

        assert responses.calls[-1].request.method == responses.POST
        assert '-----BEGIN CERTIFICATE REQUEST-----' in resp1

        # ???: Doesn't work because HmcCertificateCsr doesn't have a template?
        # Way 2
        # hmc_certificate_csr = self.system.all(
        #     '{}.{}.{}'.format(DS8K_HMC,
        #                       DS8K_HMC_CERTIFICATE,
        #                       DS8K_HMC_CERTIFICATE_CSR),
        #     rebuild_url=True)
        # hmc_certificate_csr2 = hmc_certificate_csr.create(O=O,
        #                                    OU=OU,
        #                                    C=C,
        #                                    ST=ST,
        #                                    L=L,
        #                                    email=email,
        #                                    force=force)
        # resp2, data2 = hmc_certificate_csr2.post()
        # assert responses.calls[-1].request.method == responses.POST
        # # self.assertIsInstance(data2[0], HmcCertificateCsr)
        # assert resp2.status_code == HTTPStatus.CREATED
