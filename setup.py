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

from setuptools import find_packages, setup

import pyds8k

install_requires = ['requests', 'httpretty', 'configparser', 'six']

setup(
    name='pyds8k',
    version=pyds8k.version,
    description="DS8000 Python Client",
    long_description="DS8000 RESTful API Python Client.",
    author="Zhang Wu",
    author_email="shwzhang@cn.ibm.com",
    maintainer="Zhang Wu",
    keywords=["IBM", "DS8000 Storage"],
    requires=install_requires,
    install_requires=install_requires,
    tests_require=['nose', 'mock'],
    license="Apache License, Version 2.0",
    include_package_data=True,
    packages=find_packages(),
    provides=['pyds8k'],
    url="https://github.com/IBM/pyds8k",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
