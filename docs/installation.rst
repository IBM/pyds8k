Installing / Upgrading
======================
.. highlight:: bash


**pyds8k** is in the `Python Package Index
<http://pypi.python.org/pypi/pyds8k/>`_.

Installing with pip
-------------------

We prefer `pip <http://pypi.python.org/pypi/pip>`_
to install **pyds8k** on platforms other than Windows::

  $ pip install pyds8k

To upgrade using pip::

  $ pip install --upgrade pyds8k

Installing with easy_install
----------------------------

If you must install pyds8k using
`setuptools <http://pypi.python.org/pypi/setuptools>`_ do::

  $ easy_install pyds8k

To upgrade do::

  $ easy_install -U pyds8k


Installing from source
----------------------

If you'd rather install directly from the source (i.e. to stay on the
bleeding edge), then check out the latest source from github and 
install the driver from the resulting tree::

  $ git clone https://github.com/ibm/pyds8k.git
  $ cd pyds8k
  $ pip install .

Uninstalling an old client
--------------------------

If the older **pyds8k** was installed on the system already it
will need to be removed. Run the following command to remove it::

  $ sudo pip uninstall pyds8k
