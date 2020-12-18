************
Installation
************

$ pip install questionary
#########################

To install Questionary, simply run this simple command in your terminal of
choice:

.. code-block:: console

  $ pip install questionary

Get the Source Code
###################

Questionary is actively developed on GitHub, where the code is
`always available <https://github.com/tmbo/questionary>`_.

You can either clone the public repository:

.. code-block:: console

  $ git clone git@github.com:tmbo/questionary.git

Or, download the tarball:

.. code-block:: console

  $ curl -OL https://github.com/tmbo/questionary/tarball/master
  # optionally, zipball is also available (for Windows users).

Building From Source 
####################

Questionary uses `Poetry <https://python-poetry.org/>`_ for packaging and
dependency management. If you want to build Questionary from source, you
must install Poetry first:

.. code-block:: console

  $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3

There are several other ways to install Poetry, as seen in
`the official guide <https://python-poetry.org/docs/#installation>`_.

To install Questionary and its dependencies in editable mode, execute
:code:`make install`.
