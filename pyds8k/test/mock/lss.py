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
       "server":
       {
           "status": "ok",
           "code": "CMUC00183I",
           "message": "Operation done successfully."
       },
       "counts":
       {
           "data_counts": 5,
           "total_counts": 5
       },
       "data":
       {
           "lss":
           [
               {
                   "id": "00",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/lss/00"
                   },
                   "group": "0",
                   "addrgrp": "0",
                   "type": "fb",
                   "configvols": "25",
                   "volumes":
                   {
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/"
                                   "lss/00/volumes"
                       }
                   }
               },
               {
                   "id": "02",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/"
                               "lss/02"
                   },
                   "group": "0",
                   "addrgrp": "0",
                   "type": "fb",
                   "configvols": "16",
                   "volumes":
                   {
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/"
                                   "lss/02/volumes"
                       }
                   }
               },
               {
                   "id": "04",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/lss/04"
                   },
                   "group": "0",
                   "addrgrp": "0",
                   "type": "fb",
                   "configvols": "256",
                   "volumes":
                   {
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/"
                                   "lss/04/volumes"
                       }
                   }
               },
               {
                   "id": "06",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/lss/06"
                   },
                   "group": "0",
                   "addrgrp": "0",
                   "type": "fb",
                   "configvols": "256",
                   "volumes":
                   {
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/"
                                   "lss/06/volumes"
                       }
                   }
               },
               {
                   "id": "08",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/lss/08"
                   },
                   "group": "0",
                   "addrgrp": "0",
                   "type": "fb",
                   "configvols": "256",
                   "volumes":
                   {
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/"
                                   "lss/08/volumes"
                       }
                   }
               }
           ]
       }
    }


ONE = {
       "server":
       {
           "status": "ok",
           "code": "CMUC00183I",
           "message": "Operation done successfully."
       },
       "counts":
       {
           "data_counts": 1,
           "total_counts": 1
       },
       "data":
       {
           "lss":
           [
               {
                   "id": "00",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/lss/00"
                   },
                   "group": "0",
                   "addrgrp": "0",
                   "type": "fb",
                   "configvols": "25",
                   "volumes":
                   {
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/lss/"
                                   "00/volumes"
                       }
                   }
               }
           ]
       }
    }
