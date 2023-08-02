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

from pyds8k.resources.ds8k.v1.common.types import DS8K_HMC, \
                                                  DS8K_HMC_CERTIFICATE
# from pyds8k.resources.ds8k.v1.hmc.certificate import HmcCertificate
from pyds8k.test.data import action_response_json, action_response, \
                             upload_hmc_certificate_cert
from pyds8k.test.test_resources.test_ds8k.base import TestDS8KWithConnect


class TestHmcCertificate(TestDS8KWithConnect):

    def setUp(self):
        super(TestHmcCertificate, self).setUp()

    @httpretty.activate
    def test_upload_hmc_certificate(self):
        url = '/{}/{}'.format(DS8K_HMC, DS8K_HMC_CERTIFICATE)

        def _verify_request(request, uri, headers):
            self.assertEqual(uri, self.domain + self.base_url + url)
            self.assertIn(
                upload_hmc_certificate_cert,
                request.body.decode('UTF-8')
            )
            return (201, headers, action_response_json)

        httpretty.register_uri(httpretty.POST,
                               self.domain + self.base_url + url,
                               body=_verify_request,
                               content_type='multipart/form'
                               )
        # Way 1
        resp1 = self.system.upload_hmc_signed_certificate(
                    upload_hmc_certificate_cert
                    )

        self.assertEqual(httpretty.POST, httpretty.last_request().method)
        self.assertEqual(resp1[0].status_code, 201)
        self.assertEqual(resp1[1], action_response)

        # ???: Doesn't work because HmcCertificate doesn't have a template?
        # # Way 2
        # hmc_certificate = self.system.all(
        #     '{}.{}'.format(DS8K_HMC, DS8K_HMC_CERTIFICATE),
        #     rebuild_url=True)
        # hmc_certificate2 = hmc_certificate.create(body=cert)
        # resp2, data2 = hmc_certificate_csr2.post()
        # self.assertEqual(httpretty.POST, httpretty.last_request().method)
        # # self.assertIsInstance(data2[0], HmcCertificate)
        # self.assertEqual(resp2.status_code, 201)
