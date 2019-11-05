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

GiB = 2**30     # Gibibyte = GiB = 2^30 B = 1,073,741,824 bytes
MiB = 2**20     # Mebibyte = MiB = 2^20 B = 1,048,576 bytes
KiB = 2**10     # Kibibyte = kiB = 2^10 B = 1,024 bytes

GB = 10**9      # Gigabyte = GB = 10^9 B = 1,000,000,000 bytes
MB = 10**6      # Megabyte = MB = 10^6 B = 1,000,000 bytes
KB = 10**3      # Kilobyte = kB = 10^3 B = 1,000 bytes


def validate_number(number):
    if not isinstance(number, (int, float)):
        raise ValueError("Expected types are (int, long, float)")

# =============================================================================
# Methods converting to bytes.
# =============================================================================


def convert_size_gib_to_bytes(size_in_gib):
    """:rtype: int / long"""
    validate_number(size_in_gib)
    return size_in_gib * GiB


def convert_size_mib_to_bytes(size_in_mib):
    """:rtype: int / long"""
    validate_number(size_in_mib)
    return size_in_mib * MiB


def convert_size_kib_to_bytes(size_in_kib):
    """:rtype: int / long"""
    validate_number(size_in_kib)
    return size_in_kib * KiB


def convert_size_gb_to_bytes(size_in_gb):
    """:rtype: int / long"""
    validate_number(size_in_gb)
    return size_in_gb * GB


def convert_size_mb_to_bytes(size_in_mb):
    """:rtype: int / long"""
    validate_number(size_in_mb)
    return size_in_mb * MB


def convert_size_kb_to_bytes(size_in_kb):
    """:rtype: int / long"""
    validate_number(size_in_kb)
    return size_in_kb * KB


# =============================================================================
# Methods converting from bytes.
# =============================================================================


def convert_size_bytes_to_gib(size_in_bytes):
    """:rtype: float"""
    return float(size_in_bytes) / GiB


def convert_size_bytes_to_mib(size_in_bytes):
    """:rtype: float"""
    return float(size_in_bytes) / MiB


def convert_size_bytes_to_kib(size_in_bytes):
    """:rtype: float"""
    return float(size_in_bytes) / KiB


def convert_size_bytes_to_gb(size_in_bytes):
    """:rtype: float"""
    return float(size_in_bytes) / GB


def convert_size_bytes_to_mb(size_in_bytes):
    """:rtype: float"""
    return float(size_in_bytes) / MB


def convert_size_bytes_to_kb(size_in_bytes):
    """:rtype: float"""
    return float(size_in_bytes) / KB
