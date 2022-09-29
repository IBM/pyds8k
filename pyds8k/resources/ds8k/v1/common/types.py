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

DS8K_TOKEN = 'tokens'
DS8K_SYSTEM = 'systems'
DS8K_NODE = 'nodes'
DS8K_MARRAY = 'marrays'
DS8K_USER = 'users'
DS8K_ENCRYPTION_GROUP = 'encryption_groups'
DS8K_IOENCLOSURE = 'io_enclosures'
DS8K_POOL = 'pools'
DS8K_RESOURCE_GROUP = 'resource_groups'
DS8K_TSEREP = 'tserep'
DS8K_ESEREP = 'eserep'
DS8K_LSS = 'lss'
DS8K_LCU_TYPE_3990_3 = '3990-3'
DS8K_LCU_TYPE_3990_TPF = '3990-tpf'
DS8K_LCU_TYPE_3990_6 = '3990-6'
DS8K_LCU_TYPE_bs2000 = 'bs2000'
DS8K_LCU_TYPES = (
    DS8K_LCU_TYPE_3990_3,
    DS8K_LCU_TYPE_3990_TPF,
    DS8K_LCU_TYPE_3990_6,
    DS8K_LCU_TYPE_bs2000
)
DS8K_VOLUME = 'volumes'
DS8K_SE = 'SE'
DS8K_VOLUME_GROUP = 'volgrps'
DS8K_HOST_PORT = 'host_ports'
DS8K_HOST = 'hosts'
DS8K_IOPORT = 'ioports'
DS8K_VOLMAP = 'mappings'
DS8K_EVENT = 'events'
DS8K_VOLUME_TYPE_FB = 'fb'
DS8K_VOLUME_TYPE_CKD = 'ckd'
DS8K_VOLUME_TYPES = (DS8K_VOLUME_TYPE_FB, DS8K_VOLUME_TYPE_CKD)
DS8K_LSS_TYPES = (DS8K_VOLUME_TYPE_CKD, )
DS8K_FLASHCOPY = 'flashcopy'
DS8K_PPRC = 'pprc'
DS8K_CAPTYPE_GIB = 'gib'
DS8K_CAPTYPE_BYTE = 'bytes'
DS8K_CAPTYPE_CYL = 'cyl'
DS8K_CAPTYPE_MOD1 = 'mod1'
DS8K_CAPTYPES = (DS8K_CAPTYPE_GIB,
                 DS8K_CAPTYPE_BYTE,
                 DS8K_CAPTYPE_CYL,
                 DS8K_CAPTYPE_MOD1
                 )
DS8K_TP_NONE = 'none'
DS8K_TP_ESE = 'ese'
DS8K_TP_TSE = 'tse'
DS8K_TPS = (DS8K_TP_NONE, DS8K_TP_ESE, DS8K_TP_TSE)

DS8K_COPY_SERVICE_PREFIX = 'cs'
DS8K_CS_PPRC = 'pprcs'
DS8K_CS_FLASHCOPY = 'flashcopies'

DS8K_OPTION_FRCO = "freeze_consistency"
DS8K_OPTION_ITW = "inhibit_target_writes"
DS8K_OPTION_RECH = "record_changes"
DS8K_OPTION_NBC = "no_background_copy"
DS8K_OPTION_PER = "persistent"
DS8K_OPTION_APTP = "allow_pprc_target_primary"
DS8K_OPTION_RERE = "reverse_restore"
DS8K_OPTION_FRR = "fast_reverse_restore"
DS8K_OPTION_PSET = "permit_space_efficient_target"
DS8K_OPTION_FSETOOS = "fail_space_efficient_target_out_of_space"

DS8K_FC_OPTIONS = (DS8K_OPTION_FRCO,
                   DS8K_OPTION_ITW,
                   DS8K_OPTION_RECH,
                   DS8K_OPTION_NBC,
                   DS8K_OPTION_PER,
                   DS8K_OPTION_APTP,
                   DS8K_OPTION_RERE,
                   DS8K_OPTION_FRR,
                   DS8K_OPTION_PSET,
                   DS8K_OPTION_FSETOOS)
