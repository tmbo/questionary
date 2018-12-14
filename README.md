# questionary

[![version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![license](https://img.shields.io/pypi/l/questionary.svg)](https://pypi.org/project/questionary/)
[![Build Status](https://travis-ci.com/tmbo/questionary.svg?branch=master)](https://travis-ci.com/tmbo/questionary)
[![Coverage Status](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)


Python library to build pretty command line user prompts ✨

You need input from a user, e.g. how an output file should be named or if he really wants to execute that dangerous operation? This library will help you make the input prompts easy to read and answer for the user.

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

![select](docs/images/select.png)

## Documentation

1. [Different question types](#1-Different-question-types) 
   
   The available question types are [text](#text), [password](#password), [confirm](#confirm), [select](#select), [rawselect](#rawselect) and [checkbox](#checkbox).

2. [Styling your prompts](#2-Styling-your-prompt)

   Customize how your questions look.

### 1. Different question types

#### text
    
   A free text input for the user. 
    
   ```python
   questionary.text("What's your first name").ask()
   ```
   
   ![text](docs/images/text.png)
#### password

   A free text input for the user where the input is not
   shown but replaced with `***`. 
    
   ```python
   questionary.password("What's your secret?").ask()
   ```
   
   ![password](docs/images/password.png)
#### confirm

   A yes or no question. The user can either confirm or deny. 
    
   ```python
   questionary.confirm("Are you amazed?").ask()
   ```
   
   ![confirm](docs/images/confirm.png)
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
   
   ![select](docs/images/select.png)
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

   ![rawselect](docs/images/rawselect.png)
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
   ![checkbox](docs/images/checkbox.png)

### 2. Styling your prompts

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

`questionary` is written and maintained by Tom Bocklisch. It is based on the great work of [Oyetoke Toby](https://github.com/CITGuru/PyInquirer). 

## License
Licensed under the MIT License. Copyright 2018 Tom Bocklisch. [Copy of the license](LICENSE).
