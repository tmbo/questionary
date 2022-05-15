*******************
Contributor's Guide
*******************

Steps for Submitting Code
#########################
Contributions are very much welcomed and appreciated. Every little bit of help
counts, so do not hesitate!

1. Check for open issues, or open a new issue to start some discussion around
   a feature idea or bug. There is a `contributor friendly tag`_ for issues
   that should be ideal for people who are not familiar with the codebase yet.

2. Fork `the repository <https://github.com/tmbo/questionary>`_ on GitHub to
   start making your changes.

3. `Install Poetry <https://python-poetry.org/docs/#installation>`_.

4. Configure development environment.

  .. code-block:: console

    make develop

5. Write some tests that show the bug is fixed or that the feature works as
   expected.

6. Ensure your code passes the code quality checks by running

  .. code-block:: console

    $ make lint

7. Check all of the unit tests pass by running

  .. code-block:: console

    $ make test

8. Check the type checks pass by running

  .. code-block:: console

    $ make types

9. Send a pull request and bug the maintainer until it gets merged and
   published 🙂

.. _`contributor friendly tag`: https://github.com/tmbo/questionary/issues?direction=desc&labels=good+first+issue&page=1&sort=upd

Bug Reports
###########

Bug reports should be made to the
`issue tracker <https://github.com/tmbo/questionary/issues>`_.
Please include enough information to reproduce the issue you are having.
A `minimal, reproducible example <https://stackoverflow.com/help/minimal-reproducible-example>`_
would be very helpful.

Feature Requests
################

Feature requests should be made to the
`issue tracker <https://github.com/tmbo/questionary/issues>`_.

Other
#####

Create a New Release
********************

1. Update the version number in ``questionary/version.py`` and
   ``pyproject.toml``.

2. Add a new section for the release to :ref:`changelog`.
3. Commit these changes.
4. ``git tag`` the commit with the release version number.

GitHub Actions will build and push the updated library to PyPi.

Create a Command Line Recording
*******************************

1. Install the following tools:

    .. code-block:: console

      $ brew install asciinema
      $ npm install --global asciicast2gif

2. Start the recording with ``asciinema``:

    .. code-block:: console

      $ asciinema rec

3. Do the thing you want to record.

4. Convert to gif using ``asciicast2gif``:

    .. code-block:: console

      $ asciicast2gif -h 7 -w 120 -s 2 <recording> output.gif
