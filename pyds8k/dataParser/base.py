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

from abc import ABCMeta, abstractmethod


class BaseRequestParser(object, metaclass=ABCMeta):
    """
    Parse the data user wants to send to server,
    in the right format that server defined.
    """

    @abstractmethod
    def get_raw_data(self):
        pass

    @abstractmethod
    def get_request_data(self):
        pass


class BaseResponseParser(object, metaclass=ABCMeta):
    """
    Parser response data, to get resource link, representation, etc.
    """

    response_key = ''
    success_status = ('ok', 'successful', )
    resource_data_key = 'data'
    error_status_key = 'status'

    @abstractmethod
    def get_raw_data(self):
        pass

    @abstractmethod
    def get_link(self):
        pass

    @abstractmethod
    def get_representations(self):
        pass

    @abstractmethod
    def get_posta_response_data(self):
        """
        Return a list of ({resource_data_key:resource_data}, resource_uri)
        or ({error_status_key:status_data}, None) if the rest server returns
        a partial failure response.

        For example:
        If you create two resources(res1, res2) at a time, you should return
        [({resource_data_key:res1_data}, res1_uri),
         ({error_status_key:res2_status_data}, None)
         ]
        or
        [({resource_data_key:res1_data}, res1_uri), ] if you only care about
        success ones.
        """
        pass

    @abstractmethod
    def get_status_body(self):
        pass

    @abstractmethod
    def get_error_code(self):
        pass

    @abstractmethod
    def get_error_msg(self):
        pass

    @classmethod
    @abstractmethod
    def get_link_from_representation(cls, representation):
        pass
