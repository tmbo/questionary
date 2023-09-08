.. _changelog:

*********
Changelog
*********

2.0.1 (2023-09-08)
###################

* Updated dependencies.
* Fixed broken documentation build.

2.0.0 (2023-07-25)
###################

* Updated dependencies.
* Modified default choice selection based on the ``Choice`` value. Now, it is
  not necessary to pass the same instance of the ``Choice`` object: the same
  ``value`` may be used.
* Fixed various minor bugs in development scripts and continuous integration.
* Improved continuous integration and testing process.
* Added pull request and issue templates to the GitHub repository.
* Implemented lazy function call for obtaining choices.
* Expanded the test matrix to include additional Python versions.
* Added the ability to specify the start point of a file path.
* Enabled displaying arbitrary paths in file path input.
* Allowed skipping of questions in the ``unsafe_ask`` function.
* Resolved typing bugs.
* Included a password confirmation example.
* Now returning selected choices even if they are disabled.
* Added support for Emacs keys (:kbd:`Ctrl+N` and :kbd:`Ctrl+P`).
* Fixed rendering errors in the documentation.
* Introduced a new ``print`` question type.
* Deprecated support for Python 3.6 and 3.7.
* Added dynamic instruction messages for ``checkbox`` and ``confirm``.
* Removed the upper bound from the Python version specifier.
* Added a ``press_any_key_to_continue`` prompt.

1.10.0 (2021-07-10)
###################

* Use direct image URLs in ``README.md``.
* Switched to ``poetry-core``.
* Relax Python version constraint.
* Add ``pointer`` option to ``checkbox`` and ``select``.
* Change enter instruction for multiline input.
* Removed unnecessary Poetry includes.
* Minor updates to documentation.
* Added additional unit tests.
* Added ``use_arrow_keys`` and ``use_jk_keys`` options to ``checkbox``.
* Added ``use_jk_keys`` and ``show_selected`` options to ``select``.
* Fix highlighting bug when using ``default`` parameter for ``select``.

1.9.0 (2020-12-20)
##################

* Added brand new documentation https://questionary.readthedocs.io/
  (thanks to `@kiancross <https://github.com/kiancross>`_)

1.8.1 (2020-11-17)
##################

* Fixed regression for checkboxes where all values are returned as strings
  fixes `#88 <https://github.com/tmbo/questionary/issues/88>`_.

1.8.0 (2020-11-08)
##################

* Added additional question type ``questionary.path``
* Added possibility to validate select and checkboxes selections before
  submitting them.
* Added a helper to print formatted text ``questionary.print``.
* Added API method to call prompt in an unsafe way.
* Hide cursor on select only showing the item marker.

1.7.0 (2002-10-15)
##################

* Added support for Python 3.9.
* Better UX for multiline text input.
* Allow passing custom lexer.

1.6.0 (2020-10-04)
##################

* Updated black code style formatting and fixed version.
* Fixed colour of answer for some prompts.
* Added ``py.typed`` marker file.
* Documented multiline input for devs and users and added tests.
* Accept style tuples in ``title`` argument annotation of ``Choice``.
* Added ``default`` for select and ``initial_choice`` for checkbox
  prompts.
* Removed check for choices if completer is present.

1.5.2 (2020-04-16)
##################

Bug fix release.

* Added ``.ask_async`` support for forms.

1.5.1 (2020-01-22)
##################

Bug fix release.

* Fixed ``.ask_async`` for questions on ``prompt_toolkit==2.*``.
  Added tests for it.

1.5.0 (2020-01-22)
##################

Feature release.

* Added support for ``prompt_toolkit`` 3.
* All tests will be run against ``prompt_toolkit`` 2 and 3.
* Removed support for Python 3.5 (``prompt_toolkit`` 3 does not support
  that any more).

1.4.0 (2019-11-10)
##################

Feature release.

* Added additional question type ``autocomplete``.
* Allow pointer and highlight in select question type.

1.3.0 (2019-08-25)
##################

Feature release.

* Add additional options to style checkboxes and select prompts
  `#14 <https://github.com/tmbo/questionary/pull/14>`_.

1.2.1 (2019-08-19)
##################

Bug fix release.

* Fixed compatibility with Python 3.5.2 by removing ``Type`` annotation
  (this time for real).

1.2.0 (2019-07-30)
##################

Feature release.

* Allow a user to pass in a validator as an instance
  `#10 <https://github.com/tmbo/questionary/pull/10>`_.

1.1.1 (2019-04-21)
##################

Bug fix release.

* Fixed compatibility with python 3.5.2 by removing ``Type`` annotation.

1.1.0 (2019-03-10)
##################

Feature release.

* Added ``skip_if`` to questions to allow skipping questions using a flag.

1.0.2 (2019-01-23)
##################

Bug fix release.

* Fixed odd behaviour if select is created without providing any choices
  instead, we will raise a ``ValueError`` now
  `#6 <https://github.com/tmbo/questionary/pull/6>`_.

1.0.1 (2019-01-12)
##################

Bug fix release, adding some convenience shortcuts.

* Added shortcut keys :kbd:`j` (move down the list) and :kbd:`k` (move up) to
  the prompts ``select`` and ``checkbox`` (fixes
  `#2 <https://github.com/tmbo/questionary/issues/2>`_).

* Fixed unclosed file handle in ``setup.py``.
* Fixed unnecessary empty lines moving selections to far down
  (fixes `#3 <https://github.com/tmbo/questionary/issues/3>`_).

1.0.0 (2018-12-14)
##################

Initial public release of the library.

* Added python interface.
* Added dict style question creation.
* Improved the documentation.
* More tests and automatic Travis test execution.
