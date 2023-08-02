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

import httpretty
import json

from pyds8k.dataParser.ds8k import RequestParser
from pyds8k.resources.ds8k.v1.common.types import DS8K_HMC, \
    DS8K_HMC_CERTIFICATE, \
    DS8K_HMC_CERTIFICATE_CSR
# from pyds8k.resources.ds8k.v1.hmc.certificate.csr import HmcCertificateCsr
from pyds8k.test.data import create_hmc_certificate_csr_response_json

from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestHmcCertificateCsr(TestDS8KWithConnect):

    def setUp(self):
        super(TestHmcCertificateCsr, self).setUp()

    @httpretty.activate
    def test_create_hmc_certificate_csr(self):
        url = '/{}/{}/{}'.format(
                                 DS8K_HMC,
                                 DS8K_HMC_CERTIFICATE,
                                 DS8K_HMC_CERTIFICATE_CSR
                                 )

        O = "IBM"  # noqa: E741
        OU = "DS8000"
        C = "US"
        ST = "NY"
        L = "Armok"
        email = "ansible@fake_server.com"
        force = "True"

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)

            req = RequestParser({'O': O,
                                 'OU': OU,
                                 'C': C,
                                 'ST': ST,
                                 'L': L,
                                 'email': email,
                                 'force': force
                                 })
            assert {
                    **json.loads(request.body).get('request').get('params'),
                    **req.get_request_data().get('request').get('params')
                   } == json.loads(request.body).get('request').get('params')
            return (201, headers, create_hmc_certificate_csr_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='application/json',
                               )
        # Way 1
        resp1 = self.system.create_hmc_csr(O=O,
                                           OU=OU,
                                           C=C,
                                           ST=ST,
                                           L=L,
                                           email=email,
                                           force=force)

        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertIn('-----BEGIN CERTIFICATE REQUEST-----', resp1)

        # ???: Doesn't work because HmcCertificateCsr doesn't have a template?
        # # Way 2
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
        # self.assertEqual(httpretty.POST, httpretty.last_request().method)
        # # self.assertIsInstance(data2[0], HmcCertificateCsr)
        # self.assertEqual(resp2.status_code, 201)
