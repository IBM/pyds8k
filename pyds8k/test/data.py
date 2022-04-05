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
