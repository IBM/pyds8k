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

ALL = {
  "server": {
    "status": "ok",
    "code": "CMUC00183I",
    "message": "Operation done successfully."
  },
  "counts": {
    "data_counts": 2,
    "total_counts": 2
  },
  "data": {
    "host_ports": [
      {
        "wwpn": "210000E08B10A95C",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/host_ports/210000E08B10A95C"
        },
        "state": "logged in",
        "hosttype": "VMware",
        "addrdiscovery": "lunpolling",
        "lbs": "512",
        "host": {
                 'name': 'host1',
                 'link': {
                          'rel': 'self',
                          'href': 'https://localhost:8088/api/v1/hosts/host1'
                          },
                 },
        "ioport": {
                 'id': 'I0200',
                 'link': {
                          'rel': 'self',
                          'href': 'https://localhost:8088/api/v1/ioports/I0200'
                          },
                 },
      },
      {
        "wwpn": "210000E08B13D0BF",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/host_ports/210000E08B13D0BF"
        },
        "state": "logged out",
        "hosttype": "VMware",
        "addrdiscovery": "lunpolling",
        "lbs": "512",
        "host": {
                 'name': 'host1',
                 'link': {
                          'rel': 'self',
                          'href': 'https://localhost:8088/api/v1/hosts/host1'
                          },
                 },
        "ioport": "",
      }
    ]
  }
}

ONE = {
  "server": {
    "status": "ok",
    "code": "CMUC00183I",
    "message": "Operation done successfully."
  },
  "counts": {
    "data_counts": 1,
    "total_counts": 1
  },
  "data": {
    "host_ports": [
      {
        "wwpn": "210000E08B10A95C",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/host_ports/210000E08B10A95C"
        },
        "state": "logged in",
        "hosttype": "VMware",
        "addrdiscovery": "lunpolling",
        "lbs": "512",
        "host": {
                 'name': 'host1',
                 'link': {
                          'rel': 'self',
                          'href': 'https://localhost:8088/api/v1/hosts/host1'
                          },
                 },
        "login_ports": [
            {'id': 'I0200',
             'link': {'rel': 'self',
                      'href': 'https://localhost:8088/api/v1/ioports/I0200'
                      },
             },
        ]
      },
    ]
  }
}
