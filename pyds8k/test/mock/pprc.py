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
    "data_counts": 32,
    "total_counts": 32
  },
  'data': {
    'pprc': [{
        'sourcevolume': {
            'id': '0000',
            'link': {
                'rel': 'self',
                'href': 'https://localhost:8088/api/v1/volumes/0000',
            },
        },
        'targetvolume': {
            'id': '0001',
            'link': {
                'rel': 'self',
                'href': 'https://localhost:8088/api/v1/volumes/0001',
            },
        },
        'targetsystem': {
            'id': 'remote_ds8k',
            'link': {},
        },
        'type': 'globalcopy',
        'state': 'copy_pending',
    }, {
        'sourcevolume': {
            'id': '1000',
            'link': {
                'rel': 'self',
                'href': 'https://localhost:8088/api/v1/volumes/1000',
            },
        },
        'targetvolume': {
            'id': '1001',
            'link': {
                'rel': 'self',
                'href': 'https://localhost:8088/api/v1/volumes/1001',
            },
        },
        'targetsystem': {
            'id': 'remote_ds8k',
            'link': {},
        },
        'type': 'globalcopy',
        'state': 'copy_pending',
    },
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
  'data': {
      'pprc': [
          {
              'sourcevolume': {
                  'id': '0000',
                  'link': {
                      'rel': 'self',
                      'href': 'https://localhost:8088/api/v1/volumes/0000',
                  },
              },
              'targetvolume': {
                  'id': '0001',
                  'link': {
                      'rel': 'self',
                      'href': 'https://localhost:8088/api/v1/volumes/0001',
                  },
              },
              'targetsystem': {
                  'id': 'remote_ds8k',
                  'link': {},
              },
              'type': 'globalcopy',
              'state': 'copy_pending',
          },
      ]
  }
}
