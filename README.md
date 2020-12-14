# questionary

[![version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![license](https://img.shields.io/pypi/l/questionary.svg)](https://pypi.org/project/questionary/)
![Continuous Integration](https://github.com/tmbo/questionary/workflows/Continuous%20Integration/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary?ref=badge_shield)
[![Documentation Status](https://readthedocs.org/projects/questionary/badge/?version=latest)](https://questionary.readthedocs.io/en/latest/?badge=latest)

✨ An effortless Python library to build pretty command line interfaces ✨

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

![Example](https://github.com/tmbo/questionary/blob/master/docs/images/example.gif)

Used and supported by

[<img src="https://github.com/tmbo/questionary/blob/master/docs/images/rasa-logo.svg" width="200">](https://github.com/RasaHQ/rasa)

## Features 
Do you need to get command line input from a user? You need to check that they _really_
want to execute that dangerous operation, or select some options from a predefined list
or ask the user for an output file path? This library gives you the tools to write
effortless command line input prompts, enjoyable for you, the developer, and the
user.

## Installation

`questionary` can be installed using `pip`:

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

That's all it takes to create a user prompt! There are different types of prompts, 
you'll find examples for all of them further down.

## Support

## Contributing

Contributions are highly welcomed and appreciated. Every little help counts, 
so do not hesitate!

1.  Check for open issues or open a fresh issue to start a discussion
    around a feature idea or a bug. There is a [Contributor
    Friendly](https://github.com/tmbo/questionary/issues?direction=desc&labels=good+first+issue&page=1&sort=updated&state=open)
    tag for issues that should be ideal for people who are not very
    familiar with the codebase yet.
2.  Fork [the repository](https://github.com/tmbo/questionary) on
    GitHub to start making your changes to the **master** branch (or
    branch off of it).
3.  Write a test which shows that the bug was fixed or that the feature
    works as expected.
4.  Ensure your code passes running `black questionary`.
5.  Send a pull request and bug the maintainer until it gets merged and
    published. 🙂

## Authors and Acknowledgment

questionary is written and maintained by Tom Bocklisch.

It is based on the great work by [Oyetoke Toby](https://github.com/CITGuru/PyInquirer) 
and [Mark Fink](https://github.com/finklabs/whaaaaat).

## License
Licensed under the [MIT License](https://github.com/tmbo/questionary/blob/master/LICENSE). Copyright 2020 Tom Bocklisch.

[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary?ref=badge_large)
