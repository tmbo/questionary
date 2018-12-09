# questionary

[![version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![license](https://img.shields.io/pypi/l/questionary.svg)](https://pypi.org/project/questionary/)
[![Build Status](https://travis-ci.com/tmbo/questionary.svg?branch=master)](https://travis-ci.com/tmbo/questionary)
[![Coverage Status](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)


Python library to build pretty command line user prompts ✨

## Quickstart

To install `questionary`, simply use [pipenv](http://pipenv.org/) (or pip, of
course):

```bash
$ pipenv install questionary
✨🎂✨
```

Satisfaction guaranteed. Let's create a first question:

```python
import questionary

questionary.select("What do you want to do?",
                   choices=[
                       'Order a pizza',
                       'Make a reservation',
                       'Ask for opening hours'
                   ]).ask()   # returns value of selected item
```

This will create the following list, allowing the user to choose an option:

![select](docs/images/select.png)

## Documentation



## How to Contribute

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
4.  Send a pull request and bug the maintainer until it gets merged and
    published. 🙂
    
## Contributors

`questionary` is written and maintained by Tom Bocklisch. It is based on the great work of [Oyetoke Toby](https://github.com/CITGuru/PyInquirer). 

## License
Licensed under the MIT License. Copyright 2018 Tom Bocklisch. [Copy of the license](LICENSE).
