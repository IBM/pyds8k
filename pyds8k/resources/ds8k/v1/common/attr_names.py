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

# system
SYSTEM_ID = 'id'   # 2107-{sn}
SYSTEM_CODE_LEVEL = 'bundle'
SYSTEM_NAME = 'name'
SYSTEM_MODEL = 'MTM'
SYSTEM_STATE = 'state'

# volume
VOLUME_ID = 'id'
VOLUME_NAME = 'name'
VOLUME_DATA_TYPE = 'datatype'
VOLUME_TYPE = 'stgtype'
VOLUME_SCSI_ID = ''
VOLUME_LOGICAL_CAP = ''
VOLUME_PHYSICAL_CAP = ''
VOLUME_USED_CAP = ''
VOLUME_ACCESS_STATE = 'state'
VOLUME_CONFIG_STATE = 'state'
VOLUME_DATA_STATE = 'state'
VOLUME_EXTENT_ALLOCATION_METHOD = 'allocmethod'
VOLUME_STORAGE_ALLOCATION_METHOD = 'tp'  # none|tse|ese

# pool
POOL_ID = 'id'
POOL_NAME = 'name'
POOL_PHYSICAL_SIZE = 'cap'
POOL_LOGICAL_SIZE = 'cap'
POOL_PHYSICAL_FREE = 'capavail'
POOL_LOGICAL_FREE = 'capavail'
POOL_RANK_GROUP = 'node'
POOL_EXTENT_TYPE = 'stgtype'
# POOL_ALLOCATED_CAPACITY = ''
# POOL_RESERVED_CAPACITY = ''
# POOL_VIRTUAL_CAPACITY = ''
# POOL_REAL_CAPACITY_ALLOCATED = ''
POOL_CAP_ALLOCATED_REAL_EXTS_ON_ESE = ''
POOL_CAP_ALLOCATED_VIRT_EXTS_ON_ESE = ''

# flashCopy
FC_SOURCE_VOLUME_ID = 'sourcevolume.id'
FC_TARGET_VOLUME_ID = 'targetvolume.id'
FC_STATUS = 'state'
FC_IS_PERSISTENT = 'persistent'  # enabled|disabled
FC_IS_RECORDING = 'recording'  # enabled|multinc|disabled|None
FC_IS_BGCOPY = 'backgroundcopy'  # enabled|disabled
FC_FLASH_COPY_ID = ''

# pprc
PPRC_SOURCE_VOLUME_ID = 'sourcevolume.id'
PPRC_TARGET_VOLUME_ID = 'targetvolume.id'
PPRC_SOURCE_ESS_NAME = 'system.id'
PPRC_TARGET_ESS_NAME = 'targetsystem.id'
FC_STATUS = 'state'
PPRC_REMOTE_COPY_TYPE = 'type'  # metromirror|globalcopy|unknown

# ioport
IOPORT_NAME = 'id'
IOPORT_WWPN = 'wwpn'
IOPORT_WWNN = ''
IOPORT_PORT_SPEED = 'speed'
IOPORT_STATUS = 'state'
IOPORT_LOCATION = 'loc'
IOPORT_ENCLOSURE_LOGICAL_NAME = ''

# host
HOST_ID = 'name'
