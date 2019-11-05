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
    "data_counts": 6,
    "total_counts": 6
  },
  "data": {
    "pools": [
      {
        "id": "P1",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/pools/P1"
        },
        "name": "PoolName_ckd1_b",
        "node": "1",
        "stgtype": "ckd",
        "cap": "439635",
        "capalloc": "25599",
        "capavail": "414036",
        "overprovisioned": "",
        'real_capacity_allocated_on_ese': '0',
        'virtual_capacity_allocated_on_ese': '0',
        "easytier": "none",
        "tieralloc":
               [
                   {
                       "tier": "ENT",
                       "assigned": "0",
                       "cap": "446676598784",
                       "allocated": "0"
                   }
               ],
        "threshold": "15",
        "eserep": {
          "link": {
            "rel": "self",
            "href": "https://localhost:8088/api/v1/pools/P1/eserep"
          }
        },
        "tserep": {
          "link": {
            "rel": "self",
            "href": "https://localhost:8088/api/v1/pools/P1/tserep"
          }
        },
        "volumes": ""
      },
      {
        "id": "P2",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/pools/P2"
        },
        "name": "regression",
        "node": "0",
        "stgtype": "fb",
        "cap": "512",
        "capalloc": "512",
        "capavail": "512",
        "overprovisioned": "0.6",
        'real_capacity_allocated_on_ese': '0',
        'virtual_capacity_allocated_on_ese': '0',
        "threshold": "15",
        "eserep": "",
        "tserep": {
          "link": {
            "rel": "self",
            "href": "https://localhost:8088/api/v1/pools/P2/tserep"
          }
        },
        "volumes": {
          "link": {
            "rel": "self",
            "href": "https://localhost:8088/api/v1/pools/P2/volumes"
          }
        }
      },
      {
        "id": "P3",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/pools/P3"
        },
        "name": "vPool",
        "node": "1",
        "stgtype": "ckd",
        "cap": "518658",
        "capalloc": "0",
        "capavail": "518658",
        "overprovisioned": "0.0",
        'real_capacity_allocated_on_ese': '0',
        'virtual_capacity_allocated_on_ese': '0',
        "threshold": "15",
        "eserep": "",
        "tserep": "",
        "volumes": ""
      },
      {
        "id": "P4",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/pools/P4"
        },
        "name": "p5",
        "node": "0",
        "stgtype": "fb",
        "cap": "0",
        "capalloc": "0",
        "capavail": "0",
        "overprovisioned": "",
        'real_capacity_allocated_on_ese': '0',
        'virtual_capacity_allocated_on_ese': '0',
        "easytier": "none",
        "tieralloc":
               [
                   {
                       "tier": "ENT",
                       "assigned": "0",
                       "cap": "446676598784",
                       "allocated": "0"
                   }
               ],
        "threshold": "15",
        "eserep": "",
        "tserep": "",
        "volumes": ""
      },
      {
        "id": "P6",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/pools/P6"
        },
        "name": "fb_odd",
        "node": "0",
        "stgtype": "fb",
        "cap": "0",
        "capalloc": "0",
        "capavail": "0",
        "overprovisioned": "",
        'real_capacity_allocated_on_ese': '0',
        'virtual_capacity_allocated_on_ese': '0',
        "easytier": "none",
        "tieralloc":
               [
                   {
                       "tier": "ENT",
                       "assigned": "0",
                       "cap": "446676598784",
                       "allocated": "0"
                   }
               ],
        "threshold": "15",
        "eserep": "",
        "tserep": "",
        "volumes": ""
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
    "pools": [
      {
        "id": "P1",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/pools/P1"
        },
        "name": "PoolName_ckd1_b",
        "node": "1",
        "stgtype": "ckd",
        "cap": "439635",
        "capalloc": "25599",
        "capavail": "414036",
        "overprovisioned": "",
        'real_capacity_allocated_on_ese': '0',
        'virtual_capacity_allocated_on_ese': '0',
        "easytier": "none",
        "tieralloc":
               [
                   {
                       "tier": "ENT",
                       "assigned": "0",
                       "cap": "446676598784",
                       "allocated": "0"
                   }
               ],
        "threshold": "15",
        "eserep": {
          "link": {
            "rel": "self",
            "href": "https://localhost:8088/api/v1/pools/P1/eserep"
          }
        },
        "tserep": {
          "link": {
            "rel": "self",
            "href": "https://localhost:8088/api/v1/pools/P1/tserep"
          }
        },
        "volumes": ""
      },
    ]
  }
}
