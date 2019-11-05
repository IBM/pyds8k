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
       "code": "",
       "message": "Operation done successfully."
   },
   "counts":
   {
       "data_counts": 19231,
       "total_counts": 19231
   },
   "data":
   {
       "events":
       [
           {
               "id": "SE1",
               "type": "UserLoginFailed",
               "severity": "info",
               "time": "2015-03-31T08:00:48-0700",
               "resource_id": "EHqqq92V9",
               "formatted_parameter":
               [
                   "EHqqq92V9",
                   "(2) the use of an account that does not exist",
                   "lockedfalse",
                   "1",
                   "initialPolicy"
               ],
               "description": "event details",
           },
           {
               "id": "SE2",
               "type": "UserLoginFailed",
               "severity": "info",
               "time": "2015-03-31T08:00:48-0700",
               "resource_id": "EHqqq92V9",
               "formatted_parameter":
               [
                   "EHqqq92V9",
                   "(2) the use of an account that does not exist",
                   "lockedfalse",
                   "1",
                   "initialPolicy"
               ],
               "description": "event details",
           },
           {
               "id": "SE3",
               "type": "UserLoggedOn",
               "severity": "info",
               "time": "2015-03-31T08:00:48-0700",
               "resource_id": "admin",
               "formatted_parameter":
               [
                   "admin",
                   ",Administrator",
                   "*",
                   "9.11.217.179",
                   "DSGUI",
                   "5.7.40.1303",
                   "initialPolicy",
                   "",
                   "HMCID: 1",
                   "fbb1149"
               ],
               "description": "event details",
           },
           {
               "id": "SE4",
               "type": "UserLoggedOn",
               "severity": "info",
               "time": "2015-03-31T08:00:48-0700",
               "resource_id": "admin",
               "formatted_parameter":
               [
                   "admin",
                   ",Administrator",
                   "*",
                   "9.11.217.179",
                   "DSGUI",
                   "87.40.141.0",
                   "initialPolicy",
                   "9.123.236.47",
                   "HMCID: 1",
                   "59d2965a"
               ],
               "description": "event details",
           },
        ]
    }
}


ONE = {
   "server":
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
       "events":
       [
           {
               "id": "SE1",
               "type": "UserLoginFailed",
               "severity": "info",
               "time": "2015-03-31T08:00:48-0700",
               "resource_id": "EHqqq92V9",
               "formatted_parameter":
               [
                   "EHqqq92V9",
                   "(2) the use of an account that does not exist",
                   "lockedfalse",
                   "1",
                   "initialPolicy"
               ],
               "description": "event details",
           },
        ]
    }
}
