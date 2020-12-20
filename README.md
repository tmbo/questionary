# Questionary

[![Version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![License](https://img.shields.io/pypi/l/questionary.svg)](#)
[![Continuous Integration](https://github.com/tmbo/questionary/workflows/Continuous%20Integration/badge.svg)](#)
[![Coverage Status](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)
[![Documentation Status](https://readthedocs.org/projects/questionary/badge/?version=latest)](https://questionary.readthedocs.io/en/latest/?badge=latest)

✨ Questionary is a Python library for effortlessly building pretty command line interfaces ✨

* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Documentation](#documentation)
* [Support](#support)
* [Contributing](#contributing)
* [Authors and Acknowledgment](#authors-and-acknowledgment)
* [License](#license)


![Example](https://github.com/tmbo/questionary/blob/master/docs/images/example.gif)

```python3
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
```

Used and supported by

[<img src="https://github.com/tmbo/questionary/blob/master/docs/images/rasa-logo.svg" width="200">](https://github.com/RasaHQ/rasa)

## Features

Questionary supports the following input prompts:
 
 * [Text](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#text)
 * [Password](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#password)
 * [File Path](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#file-path)
 * [Confirmation](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#confirmation)
 * [Select](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#select)
 * [Raw select](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#raw-select)
 * [Checkbox](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#checkbox)
 * [Autocomplete](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#autocomplete)

There is also a helper to [print formatted text](https://questionary.readthedocs.io/en/stable/pages/quickstart.html#printing-formatted-text)
for when you want to spice up your printed messages a bit.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Questionary:

```bash
$ pip install questionary
✨🎂✨
```

## Usage

```python
import questionary

questionary.select(
    "What do you want to do?",
    choices=[
        'Order a pizza',
        'Make a reservation',
        'Ask for opening hours'
    ]).ask()  # returns value of selection
```

That's all it takes to create a prompt! Have a [look at the documentation](https://questionary.readthedocs.io/)
for some more examples.

## Documentation

Documentation for Questionary is available [here](https://questionary.readthedocs.io/).

## Support

Please [open an issue](https://github.com/tmbo/questionary/issues/new)
with enough information for us to reproduce your problem.
A [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example)
would be very helpful.

## Contributing

Contributions are very much welcomed and appreciated. Every little bit of help
counts, so do not hesitate!

1. Check for open issues, or open a new issue to start some discussion around a
   feature idea or bug. There is a [contributor friendly tag](https://github.com/tmbo/questionary/issues?direction=desc&labels=good+first+issue&page=1&sort=upd)
   for issues that should be ideal for people who are not familiar with the codebase yet.

2. Fork [the repository](https://github.com/tmbo/questionary) on GitHub to start
   making your changes.

3. Write some tests that show the bug is fixed or that the feature works as expected.

4. Ensure your code passes the style checks by running `black questionary`.

5. Check all of the unit tests pass by running `pytest --pycodestyle --cov questionary -v`.

6. Check the type checks pass by running `mypy questionary`.

7. Send a pull request and bug the maintainer until it gets merged and
   published 🙂

## Authors and Acknowledgment

Questionary is written and maintained by Tom Bocklisch and Kian Cross.

It is based on the great work by [Oyetoke Toby](https://github.com/CITGuru/PyInquirer) 
and [Mark Fink](https://github.com/finklabs/whaaaaat).

## License
Licensed under the [MIT License](https://github.com/tmbo/questionary/blob/master/LICENSE). Copyright 2020 Tom Bocklisch.
