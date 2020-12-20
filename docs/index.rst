***********
Questionary
***********

.. image:: https://img.shields.io/pypi/v/questionary.svg
  :target: https://pypi.org/project/questionary/
  :alt: Version

.. image:: https://img.shields.io/pypi/l/questionary.svg
  :target: #
  :alt: License

.. image:: https://img.shields.io/pypi/pyversions/questionary.svg
  :target: https://pypi.python.org/pypi/questionary
  :alt: Supported Python Versions

✨ Questionary is a Python library for effortlessly building pretty command line interfaces ✨

It makes it very easy to query your user for input. You need your user to
confirm a destructive action or enter a file path? We've got you covered:

.. image:: images/example.gif

Creating your first prompt is just a few key strokes away

.. code-block:: python3

  import questionary

  first_name = questionary.text("What's your first name").ask()

This prompt will ask the user to provide free text input and the result is
stored in ``first_name``.

You can install Questionary using pip (for details, head over to the :ref:`installation` page):

.. code-block:: console

  $ pip install questionary

Ready to go? Check out the :ref:`quickstart`.

License
=======
Licensed under the `MIT License <https://github.com/tmbo/questionary/blob/master/LICENSE>`_.
Copyright 2020 Tom Bocklisch.

.. toctree::
   :hidden:
 
   pages/installation
   pages/quickstart
   pages/types
   pages/advanced
   pages/api_reference
   pages/support
   Examples <https://github.com/tmbo/questionary/tree/master/examples>

.. toctree::
   :hidden:

   pages/contributors

.. toctree::
   :hidden:

   pages/changelog
