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

ALL = {"server":
       {
           "status": "ok",
           "code": "",
           "message": "Operation done successfully."
       },
       "counts":
       {
           "data_counts": 2,
           "total_counts": 2
       },
       "data":
       {
           "users":
           [
               {
                   "name": "superuser",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/users/superuser"
                   },
                   "state": "active",
                   "group": ["Administrator"],
               },
               {
                   "name": "admin",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/users/admin"
                   },
                   "state": "active",
                   "group": ["Administrator"],
               },
           ]
       }
       }


ONE = {"server":
       {
           "status": "ok",
           "code": "",
           "message": "Operation done successfully."
       },
       "counts":
       {
           "data_counts": 1,
           "total_counts": 1
       },
       "data":
       {
           "users":
           [
               {
                   "name": "superuser",
                   "link":
                   {
                       "rel": "self",
                       "href": "https://localhost:8088/api/v1/users/superuser"
                   },
                   "state": "active",
                   "group": ["Administrator"],
               },
           ]
        }
       }
