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
       "data":
       {
           "eserep":
           [
               {
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/pools/P1/eserep"
                   },
                   "cap": "136286",
                   "capalloc": "0",
                   "capavail": "136286",
                   "overprovisioned": "0.0",
                   "repcapthreshold": "0",
                   "pool":
                   {
                       "id": "P1",
                       "link":
                       {
                           "rel": "self",
                           "href": "https://localhost:8088/api/v1/pools/P1"
                       }
                   }
               }
           ]
       }
    }

ONE = ALL
