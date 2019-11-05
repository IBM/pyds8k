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

from pyds8k.dataParser.ds8k import RequestParser, ResponseParser

AUTH_URL = '/tokens'
DEFAULT_BASE_URL = '/api/v1'


class Auth(object):

    base_url = DEFAULT_BASE_URL
    auth_url = AUTH_URL

    def __init__(self):
        pass

    @classmethod
    def authenticate(self, client):
        """
        The main authenticate method. Mandatory
        """

        params = {}
        params['username'] = client.user
        params['password'] = client.password
        if client.hostname:
            params['hmc1'] = client.hostname
        req_p = RequestParser(params)
        _, body = client.post(self.get_auth_url(),
                              body=req_p.get_request_data()
                              )
        token = _get_data(body).get('token', '')
        if token:
            client.set_defaultHeaders('X-Auth-Token', token)
            # client.set_defaultQuerystrings('token', token)

    @classmethod
    def get_auth_url(self):
        """
        Return the auth url. Mandatory
        """

        return self.base_url + self.auth_url


def _get_data(response_body):
    res_p = ResponseParser(response_body, 'token')
    return res_p.get_representations()[0]
