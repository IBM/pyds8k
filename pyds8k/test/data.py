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

import json
from .mock import success_response_one, success_response_all


def get_response_data_by_type(resource_type):
    try:
        return success_response_one[resource_type]
    except KeyError:
        raise KeyError(
            'Can not get response data by type: {}'.format(resource_type)
        )


def get_response_json_by_type(resource_type):
    try:
        return json.dumps(success_response_one[resource_type])
    except KeyError:
        raise KeyError(
            'Can not get response json by type: {}'.format(resource_type)
        )


def get_response_list_data_by_type(resource_type):
    try:
        return success_response_all[resource_type]
    except KeyError:
        raise KeyError(
            'Can not get response list data by type: {}'.format(resource_type)
        )


def get_response_list_json_by_type(resource_type):
    try:
        return json.dumps(success_response_all[resource_type])
    except KeyError:
        raise KeyError(
            'Can not get response list json by type: {}'.format(resource_type)
        )


def get_request_json_body(body):
    return json.loads(body)


# actions fail/success response
action_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
}
action_response_json = json.dumps(action_response)

action_response_failed = {
    "server": {
        "status": "failed",
        "code": "888",
        "message": "Operation done unsuccessfully."
    },
}
action_response_failed_json = json.dumps(action_response_failed)
_delete_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
}
_delete_response_json = json.dumps(_delete_response)

_put_post_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
}
_put_post_response_json = json.dumps(_put_post_response)

create_volumes_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "responses": [
        {
            "server": {
                "status": "ok",
                "code": "",
                "message": "Operation done successfully."
            },
            "data": {
                "volumes": [{"name": "lou_test1",
                             "id": "0010"
                             }
                            ]
            },
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/volumes/0010"
            }
        },
        {
            "server": {
                "status": "ok",
                "code": "",
                "message": "Operation done successfully."
            },
            "data": {
                "volumes": [{"name": "lou_test2",
                             "id": "0011"
                             }
                            ]
            },
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/volumes/0011"
            }
        },
    ]
}
create_volumes_response_json = json.dumps(create_volumes_response)

create_lss_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": ""
    },
    "data": {
        "lss": [
            {
                "id": "FE",
                "link": {
                    "rel": "self",
                    "href": "http://rest_url/v1/lss/FE"
                },
                "group": "0",
                "addrgrp": "",
                "type": "ckd",
                "sub_system_identifier": "FE00",
                "ckd_base_cu_type": "3990-6",
                "pprc_consistency_group": "disabled",
                "critical_mode": "disabled",
                "extended_long_busy_time": "120",
                "cc_session_timeout": "300",
                "xrc_session_timeout": "300",
                "configvols": "0",
                "volumes": {
                    "link": {
                        "rel": "self",
                        "href": "http://rest_url/v1/lss/FE/volumes"
                    }
                }
            }
        ]
    },
    "link": {
        "rel": "self",
        "href": "http://localhost:8080/ds8000-rest-api/v1/lss/FE"
    }
}
create_lss_response_json = json.dumps(create_lss_response)


create_volumes_partial_failed_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "responses": [
        {"server": {
            "status": "ok",
            "code": "",
            "message": "Operation done successfully."
        },
            "data": {
                "volumes": [{"name": "lou_test1",
                             "id": "0010"
                             }
                            ]
            },
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/volumes/0010"
            }
        },
        {"server": {
            "status": "failed",
            "code": "error_code",
            "message": "something wrong"
        },
        },
    ]
}
create_volumes_partial_failed_response_json = json.dumps(
    create_volumes_partial_failed_response
)

create_volume_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "data": {
        "volumes":
            [
                {
                    "name": "lou_test1",
                    "id": "0010"
                }
            ]
    },
    "link": {
        "rel": "self",
        "href": "https://localhost:8088/api/v1/volumes/0010"
    }
}
create_volume_response_json = json.dumps(create_volume_response)

create_mappings_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "responses": [
        {
            "server": {
                "status": "ok",
                "code": "",
                "message": "Operation done successfully."
            },
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/hosts/host1/mappings/00"
            }
        },
        {
            "server": {
                "status": "ok",
                "code": "",
                "message": "Operation done successfully."
            },
            "link": {
                "rel": "self",
                "href": "https://localhost:8088/api/v1/hosts/host1/mappings/01"
            }
        },
    ]
}
create_mappings_response_json = json.dumps(create_mappings_response)

create_mapping_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "link": {
        "rel": "self",
        "href": "https://localhost:8088/api/v1/hosts/host1/mappings/00"
    }
}
create_mapping_response_json = json.dumps(create_mapping_response)

create_host_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "link": {
        "rel": "self",
        "href": "https://localhost:8088/api/v1/hosts/host1"
    }
}
create_host_response_json = json.dumps(create_host_response)

create_host_port_response = {
    "server": {
        "status": "ok",
        "code": "",
        "message": "Operation done successfully."
    },
    "link": {
        "rel": "self",
        "href": "https://localhost:8088/api/v1/host_ports/210000E08B10A95C"
    }
}
create_host_port_response_json = json.dumps(create_host_port_response)

# Templates
volume_template = {'name': 'vol1',
                   'type': 'fb',
                   'lss': '00',
                   'cap': '1',
                   'sam': 'ESE',
                   'pool_id': 'P0',
                   }

default_template = {'name': 'vol1',
                    'type': 'fb',
                    'lss': '00',
                    'cap': '1',
                    'sam': 'ESE',
                    'pool_id': 'P0',
                    }

# fail response
token_response_error = {
    "server": {
        "status": "failed",
        "code": "NIServerException",
        "message": "Operation done successfully."
    }
}

# request
default_request = {
    'request': {
        'params': {
            'param1': 'test',
        }
    }
}

create_flashcopy_response = {
    'server': {
        'status': 'ok',
        'code': '',
        'message': 'Operation done successfully.'
    },
    'link': {
        'rel': 'self',
        'href': 'https:/9.151.159.203:8452/api/v1/cs/flashcopies/0000:0001'
    }
}

create_flashcopy_response_json = json.dumps(create_flashcopy_response)

create_resource_group_response = {
  "server": {
    "status": "ok",
    "code": "",
    "message": "Operation done successfully."
  },
  "data": {
    "resource_groups": [
      {
        "id": "RG1",
        "link": {
          "rel": "self",
          "href": "https://localhost:8088/api/v1/resource_groups/RG1"
        },
        "name": "group1",
        "state": "",
        "label": "group1",
        "cs_global": "",
        "pass_global": "",
        "gm_masters": [
          "00",
          "01",
          "02",
          "03",
          "04",
          "05",
          "06",
          "07",
          "08",
          "09",
          "0A",
          "0B",
          "0C",
          "0D",
          "0E",
          "0F",
          "10",
          "11",
          "12",
          "13",
          "14",
          "15",
          "16",
          "17",
          "18",
          "19",
          "1A",
          "1B",
          "1C",
          "1D",
          "1E",
          "1F",
          "20",
          "21",
          "22",
          "23",
          "24",
          "25",
          "26",
          "27",
          "28",
          "29",
          "2A",
          "2B",
          "2C",
          "2D",
          "2E",
          "2F",
          "30",
          "31",
          "32",
          "33",
          "34",
          "35",
          "36",
          "37",
          "38",
          "39",
          "3A",
          "3B",
          "3C",
          "3D",
          "3E",
          "3F",
          "40",
          "41",
          "42",
          "43",
          "44",
          "45",
          "46",
          "47",
          "48",
          "49",
          "4A",
          "4B",
          "4C",
          "4D",
          "4E",
          "4F",
          "50",
          "51",
          "52",
          "53",
          "54",
          "55",
          "56",
          "57",
          "58",
          "59",
          "5A",
          "5B",
          "5C",
          "5D",
          "5E",
          "5F",
          "60",
          "61",
          "62",
          "63",
          "64",
          "65",
          "66",
          "67",
          "68",
          "69",
          "6A",
          "6B",
          "6C",
          "6D",
          "6E",
          "6F",
          "70",
          "71",
          "72",
          "73",
          "74",
          "75",
          "76",
          "77",
          "78",
          "79",
          "7A",
          "7B",
          "7C",
          "7D",
          "7E",
          "7F",
          "80",
          "81",
          "82",
          "83",
          "84",
          "85",
          "86",
          "87",
          "88",
          "89",
          "8A",
          "8B",
          "8C",
          "8D",
          "8E",
          "8F",
          "90",
          "91",
          "92",
          "93",
          "94",
          "95",
          "96",
          "97",
          "98",
          "99",
          "9A",
          "9B",
          "9C",
          "9D",
          "9E",
          "9F",
          "A0",
          "A1",
          "A2",
          "A3",
          "A4",
          "A5",
          "A6",
          "A7",
          "A8",
          "A9",
          "AA",
          "AB",
          "AC",
          "AD",
          "AE",
          "AF",
          "B0",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "B6",
          "B7",
          "B8",
          "B9",
          "BA",
          "BB",
          "BC",
          "BD",
          "BE",
          "BF",
          "C0",
          "C1",
          "C2",
          "C3",
          "C4",
          "C5",
          "C6",
          "C7",
          "C8",
          "C9",
          "CA",
          "CB",
          "CC",
          "CD",
          "CE",
          "CF",
          "D0",
          "D1",
          "D2",
          "D3",
          "D4",
          "D5",
          "D6",
          "D7",
          "D8",
          "D9",
          "DA",
          "DB",
          "DC",
          "DD",
          "DE",
          "DF",
          "E0",
          "E1",
          "E2",
          "E3",
          "E4",
          "E5",
          "E6",
          "E7",
          "E8",
          "E9",
          "EA",
          "EB",
          "EC",
          "ED",
          "EE",
          "EF",
          "F0",
          "F1",
          "F2",
          "F3",
          "F4",
          "F5",
          "F6",
          "F7",
          "F8",
          "F9",
          "FA",
          "FB",
          "FC",
          "FD",
          "FE",
          "FF"
        ],
        "gm_sessions": [
          "00",
          "01",
          "02",
          "03",
          "04",
          "05",
          "06",
          "07",
          "08",
          "09",
          "0A",
          "0B",
          "0C",
          "0D",
          "0E",
          "0F",
          "10",
          "11",
          "12",
          "13",
          "14",
          "15",
          "16",
          "17",
          "18",
          "19",
          "1A",
          "1B",
          "1C",
          "1D",
          "1E",
          "1F",
          "20",
          "21",
          "22",
          "23",
          "24",
          "25",
          "26",
          "27",
          "28",
          "29",
          "2A",
          "2B",
          "2C",
          "2D",
          "2E",
          "2F",
          "30",
          "31",
          "32",
          "33",
          "34",
          "35",
          "36",
          "37",
          "38",
          "39",
          "3A",
          "3B",
          "3C",
          "3D",
          "3E",
          "3F",
          "40",
          "41",
          "42",
          "43",
          "44",
          "45",
          "46",
          "47",
          "48",
          "49",
          "4A",
          "4B",
          "4C",
          "4D",
          "4E",
          "4F",
          "50",
          "51",
          "52",
          "53",
          "54",
          "55",
          "56",
          "57",
          "58",
          "59",
          "5A",
          "5B",
          "5C",
          "5D",
          "5E",
          "5F",
          "60",
          "61",
          "62",
          "63",
          "64",
          "65",
          "66",
          "67",
          "68",
          "69",
          "6A",
          "6B",
          "6C",
          "6D",
          "6E",
          "6F",
          "70",
          "71",
          "72",
          "73",
          "74",
          "75",
          "76",
          "77",
          "78",
          "79",
          "7A",
          "7B",
          "7C",
          "7D",
          "7E",
          "7F",
          "80",
          "81",
          "82",
          "83",
          "84",
          "85",
          "86",
          "87",
          "88",
          "89",
          "8A",
          "8B",
          "8C",
          "8D",
          "8E",
          "8F",
          "90",
          "91",
          "92",
          "93",
          "94",
          "95",
          "96",
          "97",
          "98",
          "99",
          "9A",
          "9B",
          "9C",
          "9D",
          "9E",
          "9F",
          "A0",
          "A1",
          "A2",
          "A3",
          "A4",
          "A5",
          "A6",
          "A7",
          "A8",
          "A9",
          "AA",
          "AB",
          "AC",
          "AD",
          "AE",
          "AF",
          "B0",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "B6",
          "B7",
          "B8",
          "B9",
          "BA",
          "BB",
          "BC",
          "BD",
          "BE",
          "BF",
          "C0",
          "C1",
          "C2",
          "C3",
          "C4",
          "C5",
          "C6",
          "C7",
          "C8",
          "C9",
          "CA",
          "CB",
          "CC",
          "CD",
          "CE",
          "CF",
          "D0",
          "D1",
          "D2",
          "D3",
          "D4",
          "D5",
          "D6",
          "D7",
          "D8",
          "D9",
          "DA",
          "DB",
          "DC",
          "DD",
          "DE",
          "DF",
          "E0",
          "E1",
          "E2",
          "E3",
          "E4",
          "E5",
          "E6",
          "E7",
          "E8",
          "E9",
          "EA",
          "EB",
          "EC",
          "ED",
          "EE",
          "EF",
          "F0",
          "F1",
          "F2",
          "F3",
          "F4",
          "F5",
          "F6",
          "F7",
          "F8",
          "F9",
          "FA",
          "FB",
          "FC",
          "FD",
          "FE",
          "FF"
        ]
      }
    ]
  },
  "link": {
    "rel": "self",
    "href": "https://localhost:8088/api/v1/resource_groups/RG1"
  }
}
create_resource_group_response_json = \
    json.dumps(create_resource_group_response)
