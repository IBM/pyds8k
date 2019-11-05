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
  "data": {
    "ioports": [
      {
        "id": "I0200",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/ioports/I0200"
        },
        "state": "Online",
        "protocol": "SCSI-FCP",
        "wwpn": "500507630310003D",
        "type": "Fibre Channel-SW",
        "speed": "8 Gb/s",
        "loc": "U1400.1B3.44001B3-P1-C1-T0",
        "io_enclosure": {
            "id": "2",
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/io_enclosures/2"
                },
        }
      },
      {
        "id": "I0201",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/ioports/I0201"
        },
        "state": "Online",
        "protocol": "SCSI-FCP",
        "wwpn": "500507630310403D",
        "type": "Fibre Channel-SW",
        "speed": "8 Gb/s",
        "loc": "U1400.1B3.44001B3-P1-C1-T1",
        "io_enclosure": {
            "id": "2",
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/io_enclosures/2"
                },
        }
      },
      {
        "id": "I0202",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/ioports/I0202"
        },
        "state": "Online",
        "protocol": "SCSI-FCP",
        "wwpn": "500507630310803D",
        "type": "Fibre Channel-SW",
        "speed": "8 Gb/s",
        "loc": "U1400.1B3.44001B3-P1-C1-T2",
        "io_enclosure": {
            "id": "2",
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/io_enclosures/2"
                },
        }
      },
      {
        "id": "I0336",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/ioports/I0336"
        },
        "state": "Offline",
        "protocol": "SCSI-FCP",
        "wwpn": "50050763035B803D",
        "type": "Fibre Channel-LW",
        "speed": "8 Gb/s",
        "loc": "U1400.1B4.44001B4-P1-C4-T6",
        "io_enclosure": {
            "id": "2",
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/io_enclosures/2"
                },
        }
      },
      {
        "id": "I0337",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/ioports/I0337"
        },
        "state": "Offline",
        "protocol": "SCSI-FCP",
        "wwpn": "50050763035BC03D",
        "type": "Fibre Channel-LW",
        "speed": "8 Gb/s",
        "loc": "U1400.1B4.44001B4-P1-C4-T7",
        "io_enclosure": {
            "id": "2",
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/io_enclosures/2"
                },
        }
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
    "ioports": [
      {
        "id": "I0200",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/ioports/I0200"
        },
        "state": "Online",
        "protocol": "SCSI-FCP",
        "wwpn": "500507630310003D",
        "type": "Fibre Channel-SW",
        "speed": "8 Gb/s",
        "loc": "U1400.1B3.44001B3-P1-C1-T0",
        "io_enclosure": {
            "id": "2",
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/io_enclosures/2"
                },
        }
      }
    ]
  }
}
