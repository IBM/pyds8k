# DS8000 Python Client

[![Build Status](https://travis-ci.com/IBM/pyds8k.svg?branch=develop)](https://travis-ci.com/IBM/pyds8k)

This repository contains the IBM RESTful API Python client, which establishes terminal connection with IBM DS8000 storage systems. The Python client protocol enables full management and monitoring of these storage arrays by issuing dedicated RESTful APIs.

## Python Compatibility

The content in this collection supports Python 3.6 and newer.

## Getting started

Clone the repository, and then add it to your PYTHONPATH directory. The Python client is then ready for import and use.

## Usage examples

Usage examples of the Python client are available in the **examples.py** file.

## Displaying the RESTful APIs reference information

Each storage system of DS8000 and major software version has its own set of RESTful APIs. The RESTful APIs are detailed in the RESTful API reference guides that are available on IBM Knowledge Center (KC).

To display the full RESTful API Reference Guide of a specific storage system and a specific software version:

1.	Navigate to a storage system welcome page on KC:


2. On the welcome page, select a storage system software version. For example, select **Version 8.5.3**.

![Software version](https://github.com/IBM/pyds8k/blob/master/images/1.jpg)

The welcome page of the selected software version is displayed.

3. If needed, select the **Table of contents** tab.

![Table of contents](https://github.com/IBM/pyds8k/blob/master/images/2.jpg)

4. On the table of contents, click **RESTful API**.

![CLI interface](https://github.com/IBM/pyds8k/blob/master/images/3.jpg)

5.	Refer to **Host commands** and to all subsequent chapters.

## Contributing
We do not accept any contributions at the moment. This may change in the future, so you can fork, clone, and suggest a pull request.

## Running tests
Use nosetests command to run a test.

    nosetests -v
