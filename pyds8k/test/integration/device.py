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

from collections import namedtuple

Device = namedtuple('Device', ['ipaddr', 'username', 'password', 'port'])

ds44 = Device(ipaddr='9.11.108.44',
              username='admin',
              password='open1sys',
              port=8452
              )

ds179 = Device(ipaddr='9.11.217.179',
               username='admin',
               password='passw0rd',
               port=8452
               )
