***************
Release History
***************

1.8.1 (2020-11-17)
##################

* Fixed regression for checkboxes where all values are returned as strings
  fixes `#88 <https://github.com/tmbo/questionary/issues/88>`_.

1.8.0 (2020-11-08)
##################

* Added additional question type :code:`questionary.path`
* Added possibility to validate select and checkboxes selections before
  submitting them.
* Added a helper to print formatted text :code:`questionary.print`.
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
* Added :code:`py.typed` marker file.
* Documented multiline input for devs and users and added tests.
* Accept style tuples in :code:`title` argument annotation of :code:`Choice`.
* Added :code:`default` for select and :code:`initial_choice` for checkbox
  prompts.
* Removed check for choices if completer is present.

1.5.2 (2020-04-16)
##################

Bug fix release.

* Added :code:`.ask_async` support for forms.

1.5.1 (2020-01-22)
##################

Bug fix release.

* Fixed :code:`.ask_async` for questions on :code:`prompt_toolkit==2.*`.
  Added tests for it.

1.5.0 (2020-01-22)
##################

Feature release.

* Added support for :code:`prompt_toolkit` 3.
* All tests will be run against :code:`prompt_toolkit` 2 and 3.
* Removed support for Python 3.5 (:code:`prompt_toolkit` 3 does not support
  that anymore).

1.4.0 (2019-11-10)
##################

Feature release.

* Added additional question type :code:`autocomplete`.
* Allow pointer and highlight in select question type.

1.3.0 (2019-08-25)
##################

Feature release.

* Add additional options to style checkboxes and select prompts
  `#14 <https://github.com/tmbo/questionary/pull/14>`_.

1.2.1 (2019-08-19)
##################

Bug fix release.

* Fixed compatibility with Python 3.5.2 by removing `Type` annotation (this
  time for real).

1.2.0 (2019-07-30)
##################

Feature release.

* Allow a user to pass in a validator as an instance
  `#10 <https://github.com/tmbo/questionary/pull/10>`_.

1.1.1 (2019-04-21)
##################

Bug fix release.

* Fixed compatibility with python 3.5.2 by removing :code:`Type` annotation.

1.1.0 (2019-03-10)
##################

Feature release.

* Added :code:`skip_if` to questions to allow skipping questions using a flag.

1.0.2 (2019-01-23)
##################

Bug fix release.

* Fixed odd behaviour if select is created without providing any choices
  instead, we will raise a `ValueError` now
  `#6 <https://github.com/tmbo/questionary/pull/6>`_.

1.0.1 (2019-01-12)
##################

Bug fix release, adding some convenience shortcuts.

* Added shortcut keys :kbd:`j` (move down the list) and :kbd:`k` (move up) to
  the prompts `select` and `checkbox` (fixes
  `#2 <https://github.com/tmbo/questionary/issues/2>`_.

* Fixed unclosed file handle in :code:`setup.py`.
* Fixed unnecessary empty lines moving selections to far down
  (fixes `#3 <https://github.com/tmbo/questionary/issues/3>`_.

1.0.0 (2018-12-14)
##################

Initial public release of the library.

* Added python interface.
* Added dict style question creation.
* Improved the documentation.
* More tests and automatic travis test execution.
