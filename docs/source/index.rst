*************************
Questionary Documentation
*************************

.. image:: https://img.shields.io/pypi/v/questionary.svg
  :target: https://pypi.org/project/questionary/
  :alt: Version

.. image:: https://img.shields.io/pypi/l/questionary.svg
  :target: #
  :alt: License

.. image:: https://github.com/tmbo/questionary/workflows/Continuous%20Integration/badge.svg
  :target: #
  :alt: Continuous Integration

.. image:: https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master
  :target: https://coveralls.io/github/tmbo/questionary?branch=master
  :alt: Coverage Status

.. image:: https://img.shields.io/pypi/pyversions/questionary.svg
  :target: https://pypi.python.org/pypi/questionary
  :alt: Supported Python Versions

.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary.svg?type=shield
  :target: https://app.fossa.io/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary?ref=badge_shield
  :alt: FOSSA Status

.. image:: https://readthedocs.org/projects/questionary/badge/?version=stable
  :target: https://questionary.readthedocs.io/en/latest/?badge=stable
  :alt: Documentation Status

✨ Questionary is a Python library for effortlessly building pretty command
   line interfaces ✨

.. image:: ../images/example.gif

.. code-block:: python3

  import questionary

  questionary.text("What's your first name").ask()
  questionary.password("What's your secret?").ask()
  questionary.confirm("Are you amazed?").ask()

  questionary.select(
      "What do you want to do?",
      choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
  ).ask()

  questionary.rawselect(
      "What do you want to do?",
      choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
  ).ask()

  questionary.checkbox(
      "Select toppings", choices=["foo", "bar", "bazz"]
  ).ask()

  questionary.path("Path to the projects version file").ask()

License
=======
Licensed under the `MIT License <https://github.com/tmbo/questionary/blob/master/LICENSE>`_.
Copyright 2020 Tom Bocklisch.

The User Guide
==============

.. toctree::
   :maxdepth: 2
 
   pages/installation
   pages/quickstart
   pages/advanced
   pages/api_reference
   pages/support
   Examples <https://github.com/tmbo/questionary/tree/master/examples>

The Contributor's Guide
=======================

.. toctree::
   :maxdepth: 2

   pages/contributors

Other
=====

.. toctree::
   :maxdepth: 2

   pages/release_history
