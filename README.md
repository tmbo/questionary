# Questionary 🤔

[![Version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![License](https://img.shields.io/pypi/l/questionary.svg)](#)
[![Continuous Integration](https://github.com/tmbo/questionary/workflows/Continuous%20Integration/badge.svg)](#)
[![Coverage](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)
[![Documentation](https://readthedocs.org/projects/questionary/badge/?version=latest)](https://questionary.readthedocs.io/en/latest/?badge=latest)

✨ Questionary is a Python library for effortlessly building pretty command line interfaces ✨

* ✨ [Features](#features)           
* 🔨 [Installation](#installation)   
* 💻 [Usage](#usage)                 
* 📕 [Documentation](#documentation) 
* 💬 [Support](#support)             


![Example](https://raw.githubusercontent.com/tmbo/questionary/master/docs/images/example.gif)

```python3
import questionary # import queustionary module

questionary.text("What's your first name").ask()    # A regular text input
questionary.password("What's your secret?").ask()   # A password/sectet input
questionary.confirm("Are you amazed?").ask()        # A yes/no question

questionary.select(
    "What do you want to do?",                                                  # The initial question asked
    choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],   # Choices can have unlimited amount of items
).ask()

questionary.rawselect(
    "What do you want to do?",                                                  # Unlike normal lists, you use numbers to select the item.
    choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],   # Again, you can have unlimited amount of options here.
).ask()

questionary.checkbox(
    "Select toppings", choices=["foo", "bar", "bazz"]                           # This allows users to select more than one choice using the given controls
).ask()

questionary.path("Path to the projects version file").ask()                     # A path input
```

Used and supported by

[<img src="https://raw.githubusercontent.com/tmbo/questionary/master/docs/images/rasa-logo.svg" width="200">](https://github.com/RasaHQ/rasa)

## Features

Questionary supports the following input prompts:
 
 * [Text](https://questionary.readthedocs.io/en/stable/pages/types.html#text)
 * [Password](https://questionary.readthedocs.io/en/stable/pages/types.html#password)
 * [File Path](https://questionary.readthedocs.io/en/stable/pages/types.html#file-path)
 * [Confirmation](https://questionary.readthedocs.io/en/stable/pages/types.html#confirmation)
 * [Select](https://questionary.readthedocs.io/en/stable/pages/types.html#select)
 * [Raw select](https://questionary.readthedocs.io/en/stable/pages/types.html#raw-select)
 * [Checkbox](https://questionary.readthedocs.io/en/stable/pages/types.html#checkbox)
 * [Autocomplete](https://questionary.readthedocs.io/en/stable/pages/types.html#autocomplete)

There is also a helper to [print formatted text](https://questionary.readthedocs.io/en/stable/pages/types.html#printing-formatted-text)
for when you want to spice up your printed messages a bit.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Questionary:

```bash
pip install questionary
```
✨🎂✨

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

Contributions are very much welcomed and appreciated. Head over to the documentation on [how to contribute](https://questionary.readthedocs.io/en/stable/pages/contributors.html#steps-for-submitting-code).

## Authors and Acknowledgment

Questionary is written and maintained by Tom Bocklisch and Kian Cross.

It is based on the great work by [Oyetoke Toby](https://github.com/CITGuru/PyInquirer) 
and [Mark Fink](https://github.com/finklabs/whaaaaat).

## License
Licensed under the [MIT License](https://github.com/tmbo/questionary/blob/master/LICENSE). Copyright 2021 Tom Bocklisch.
