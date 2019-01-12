# questionary

[![version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![license](https://img.shields.io/pypi/l/questionary.svg)](https://pypi.org/project/questionary/)
[![Build Status](https://travis-ci.com/tmbo/questionary.svg?branch=master)](https://travis-ci.com/tmbo/questionary)
[![Coverage Status](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)


Python library to build pretty command line user prompts ✨

You need input from a user, e.g. how an output file should be named or if he really wants to execute that dangerous operation? This library will help you make the input prompts easy to read and answer for the user.

Used and Supported by: 

[<img src="https://rasa.com/docs/_static/rasa_logo.svg" width="60">](https://github.com/RasaHQ/rasa_core)

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

questionary.select(
    "What do you want to do?",
    choices=[
        'Order a pizza',
        'Make a reservation',
        'Ask for opening hours'
    ]).ask()  # returns value of selection
```

This will create the following list, allowing the user to choose an option:

<img src="docs/images/example.gif" width="800">

## Documentation

1. [Different question types](#1-Different-question-types) 
   
   The available question types are [text](#text), [password](#password), [confirm](#confirm), [select](#select), [rawselect](#rawselect) and [checkbox](#checkbox).

2. [Dict style question formulation](#2-Dict-style-question-formulation)

   Alterative style to create questions using a configuration dictionary. 

3. [Styling your prompts](#3-Styling-your-prompts)

   Customize how your questions look.

### 1. Different question types

#### text
    
   A free text input for the user. 
    
   ```python
   questionary.text("What's your first name").ask()
   ```
   <img src="docs/images/text.png" width="500">

#### password

   A free text input for the user where the input is not
   shown but replaced with `***`. 
    
   ```python
   questionary.password("What's your secret?").ask()
   ```
   
   <img src="docs/images/password.png" width="500">

#### confirm

   A yes or no question. The user can either confirm or deny. 
    
   ```python
   questionary.confirm("Are you amazed?").ask()
   ```
   
   <img src="docs/images/confirm.png" width="500">

#### select

   A list of items to select a choice from. The user can pick
   one option and confirm it.
    
   ```python
   questionary.select(
       "What do you want to do?",
       choices=[
           "Order a pizza",
           "Make a reservation",
           "Ask for opening hours"
       ]).ask()
   ```
   
   <img src="docs/images/select.png" width="500">

#### rawselect

   A list of items to select a choice from. The user can pick
   one option using shortcuts and confirm it.

   ```python
   questionary.rawselect(
       "What do you want to do?",
       choices=[
           "Order a pizza",
           "Make a reservation",
           "Ask for opening hours"
       ]).ask()
   ```

   <img src="docs/images/rawselect.png" width="500">

#### checkbox

   A list of items to select multiple choices from. The user can pick
   none, one or multiple options and confirm the selection.

   ```python
   questionary.checkbox(
       'Select toppings',
       choices=[
           "foo",
           "bar",
           "bazz"
       ]).ask()
   ```
   <img src="docs/images/checkbox.png" width="700">

### 2. Dict style question formulation

Instead of creating questions using the python functions, you can also create them using a configuration dictionary. 
```python
questions = [
    {
        'type': 'text',
        'name': 'phone',
        'message': "What's your phone number",
    },
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    }
]

answers = prompt(questions)
```

The returned `answers` will be a dict containing the responses, e.g. `{"phone": "0123123", "continue": False, ""}`. The questions will be prompted one after another and `prompt` will return once all of them are answered.

### 3. Styling your prompts

You can customize all the colors used for the prompts. Every part of the prompt has an identifier, which you can use to style it. Let's create our own custom style:
```python
from prompt_toolkit.styles import Style

custom_style_fancy = Style([
    ('qmark', 'fg:#673ab7 bold'),     # token in front of the question
    ('question', 'bold'),             # question text
    ('answer', 'fg:#f44336 bold'),    # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),   # pointer used in select and checkbox prompts
    ('selected', 'fg:#cc5454'),       # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),      # separator in lists
    ('instruction', '')               # user instructions for select, rawselect, checkbox
])
```

To use our custom style, we need to pass it to the question type:
```python
questionary.text("What's your phone number", style=custom_style_fancy).ask()
```

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

`questionary` is written and maintained by Tom Bocklisch. 

It is based on the great work of [Oyetoke Toby](https://github.com/CITGuru/PyInquirer) as well as the work from [Mark Fink](https://github.com/finklabs/whaaaaat). 

## Changelog

#### unreleased (master branch)

#### 1.0.1 
Bug fix release, adding some convenience shortcuts.

Release Date: 12.01.19

* Added shortcut keys `j` (move down^ the list) and `k` (move up) to
  the prompts `select` and `checkbox` (fixes [#2](https://github.com/tmbo/questionary/issues/2))
  

* Fixed unclosed file handle in `setup.py`
* Fixed unecessary empty lines moving selections to far down (fixes [#3](https://github.com/tmbo/questionary/issues/3))

#### 1.0.0 
Initial public release of the library

Release Date: 14.12.18

* Added python interface
* Added dict style question creation
* Improved the documentation
* More tests and automatic travis test execution

## License
Licensed under the MIT License. Copyright 2018 Tom Bocklisch. [Copy of the license](LICENSE).
