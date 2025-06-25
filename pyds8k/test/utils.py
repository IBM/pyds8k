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

import sys
from contextlib import contextmanager
from io import StringIO
from pathlib import Path


@contextmanager
def capture_sys_stderr_and_return(command, *args, **kwargs):
    err, sys.stderr = sys.stderr, StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err


def get_mocks(path):
    """Get a set of mock file names.

    Args:
        path (str): The file path

    Returns:
        set: A set containing mock names.
    """
    _path = Path(path).parent.absolute()
    return {
        resource.stem
        for resource in _path.iterdir()
        if resource.is_file() and not resource.stem.startswith('__init__')
    }


def get_dir_mocks(path):
    """Get a list of mock directory names.

    Args:
        path (str): The file path

    Returns:
        list: A list of directory names.
    """
    _path = Path(path).parent.absolute()
    return [
        resource.name
        for resource in _path.iterdir()
        if resource.is_dir() and resource.name != '__pycache__'
    ]
