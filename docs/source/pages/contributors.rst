*******************
Contributor's Guide
*******************

Steps for Submitting Code
#########################
Contributions are very much welcomed and appreciated. Every little bit of help
counts, so do not hesitate!

1. Check for open issues, or open a new issue to start some discussion around a
   feature idea or bug. There is a `Contributor Friendly tag`_ for issues that
   should be ideal for people who are not familiar with the codebase yet.

2. Fork `the repository <https://github.com/tmbo/questionary>`_ on GitHub to start
   making your changes.

3. Write some tests that show the bug is fixed or that the feature works as expected.

4. Ensure your code passes the style checks by running :code:`black questionary`.

5. Check all of the unit tests pass by running :code:`pytest --pycodestyle --cov questionary -v`.

6. Check the type checks pass by running :code:`mypy questionary`.

7. Send a pull request and bug the maintainer until it gets merged and
   published 🙂

.. _`Contributor Friendly tag`: https://github.com/tmbo/questionary/issues?direction=desc&labels=good+first+issue&page=1&sort=upd

Bug Reports
###########

Bug reports should be made to the
`issue tracker <https://github.com/tmbo/questionary/issues>`_.
Please include enough information to reproduce any issues you are having.
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

1. Update the version number in :code:`questionary/version.py` and
   :code:`pyproject.toml`.

2. Add a new section for the release to the :ref:`pages/release_history:release history`.
3. Commit these changes.
4. :code:`git tag` the commit with the release version number.

GitHub Actions will build and push the updated library to PyPi.

Create a Command Line Recording
*******************************

1. Install :code:`brew install asciinema` and
   :code:`npm install --global asciicast2gif`.

2. Run :code:`asciinema rec`.
3. Do the thing.
4. Convert to gif :code:`asciicast2gif -h 7 -w 120 -s 2 <recoding> output.gif`.
