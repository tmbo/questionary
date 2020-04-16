# questionary

[![version](https://img.shields.io/pypi/v/questionary.svg)](https://pypi.org/project/questionary/)
[![license](https://img.shields.io/pypi/l/questionary.svg)](https://pypi.org/project/questionary/)
[![Build Status](https://travis-ci.com/tmbo/questionary.svg?branch=master)](https://travis-ci.com/tmbo/questionary)
[![Coverage Status](https://coveralls.io/repos/github/tmbo/questionary/badge.svg?branch=master)](https://coveralls.io/github/tmbo/questionary?branch=master)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/questionary.svg)](https://pypi.python.org/pypi/questionary)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary?ref=badge_shield)

✨An easy to use python library to build pretty command line user prompts ✨

![example-gif](docs/images/example.gif)

You need input from a user, e.g. how an output file should be named or if he really wants to execute that dangerous operation? This library will help you make the input prompts easy to read and answer for the user.

Used and Supported by:

[<img src="https://rasa.com/docs/_static/rasa_logo.svg" width="60">](https://github.com/RasaHQ/rasa)

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

That's all it takes to create a user prompt! There are differen types of prompts, you'll find examples for all of them further down.

## Documentation

### Different question types

<details><summary>text</summary>

   A free text input for the user.

   ```python
   questionary.text("What's your first name").ask()
   ```
   ![example-gif](docs/images/text.gif)

</details>
<details><summary>password</summary>

   A free text input for the user where the input is not
   shown but replaced with `***`.

   ```python
   questionary.password("What's your secret?").ask()
   ```

   ![example-gif](docs/images/password.gif)

</details>
<details><summary>confirm</summary>

   A yes or no question. The user can either confirm or deny.

   ```python
   questionary.confirm("Are you amazed?").ask()
   ```

   ![example-gif](docs/images/confirm.gif)

</details>
<details><summary>select</summary>

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

   ![example-gif](docs/images/select.gif)

</details>
<details><summary>rawselect</summary>

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

   ![example-gif](docs/images/rawselect.gif)

</details>

<details><summary>checkbox</summary>

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
   ![example-gif](docs/images/checkbox.gif)

</details>

<details><summary>autocomplete</summary>

   Text input with autocomplete help.

   ```python
   questionary.autocomplete(
       'Choose ant specie',
       choices=[
            'Camponotus pennsylvanicus',
            'Linepithema humile',
            'Eciton burchellii',
            "Atta colombica",
            'Polyergus lucidus',
            'Polyergus rufescens',
       ]).ask()
   ```
   ![example-gif](docs/images/autocomplete.gif)

</details>

### Additional Features
<details><summary>Skipping questions using conditions</summary>

Sometimes it is helpful to e.g. provide a command line flag to your app
to skip any prompts, to avoid the need for an if around any question you
can pass that flag when you create the question:

```python
DISABLED = True

response = questionary.confirm("Are you amazed?").skip_if(DISABLED, default=True).ask()
```

If the condition (in this case `DISABLED`) is `True`, the question will be
skipped and the default value gets returned, otherwise the user will be
prompted as usual and the default value will be ignored.
</details>

<details><summary>Alternative style to create questions using a configuration dictionary</summary>

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

Each configuration dictionary needs to contain the following keys:

* `'type'` - The type of the question.
* `'name'` - The name of the question (will be used as key in the `answers` dictionary)
* `'message'` - Message that will be shown to the user

Optional Keys:

* `'qmark'` - Question mark to use - defaults to `?`.
* `'default'` - Preselected value.
* `'choices'` - List of choices (applies when `'type': 'select'`) or function returning a list of choices.
* `'when'` - Function checking if this question should be shown or skipped (same functionality than `.skip_if()`).
* `'validate'` - Function or Validator Class performing validation (will be performed in real time as users type).
* `filter` - Receive the user input and return the filtered value to be used inside the program. 

</details>

<details><summary>Advanced workflow examples</summary>
Questionary allows creating quite complex workflows when combining all of the above concepts.

``` python
from questionary import Separator, prompt
questions = [
    {
        'type': 'confirm',
        'name': 'conditional_step',
        'message': 'Would you like the next question?',
        'default': True,
    },
    {
        'type': 'text',
        'name': 'next_question',
        'message': 'Name this library?',
        # Validate if the first question was answered with yes or no
        'when': lambda x: x['conditional_step'],
        # Only accept questionary as answer
        'validate': lambda val: val == 'questionary'
    },
    {
        'type': 'select',
        'name': 'second_question',
        'message': 'Select item',
        'choices': [
            'item1',
            'item2',
            Separator(),
            'other',
        ],
    },
    {
        'type': 'text',
        'name': 'second_question',
        'message': 'Insert free text',
        'when': lambda x: x['second_question'] == 'other'
    },
]
prompt(questions)
```

The above workflow will show to the user as follows:
1. Yes/No question `Would you like the next question?`.
2. `Name this library?` - only shown when the first question is answered with yes
3. A question to select an item from a list.
4. Free text inpt if `'other'` is selected in step 3.

Depending on the route the user took, the result will look as follows:

``` python
{ 
    'conditional_step': False,
    'second_question': 'Testinput'   # Free form text
}
```
``` python
{ 
    'conditional_step': True,
    'next_question': 'questionary',
    'second_question': 'Testinput'   # Free form text
}
```

You can test this workflow yourself by running the [advanced_workflow.py example](https://github.com/tmbo/questionary/blob/master/examples/advanced_workflow.py).

</details>

<details><summary>Styling your prompts with your favorite colors</summary>

You can customize all the colors used for the prompts. Every part of the prompt has an identifier, which you can use to style it. Let's create our own custom style:
```python
from prompt_toolkit.styles import Style

custom_style_fancy = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#f44336 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
```

To use our custom style, we need to pass it to the question type:
```python
questionary.text("What's your phone number", style=custom_style_fancy).ask()
```

It is also possible to use a list of token tuples as a `Choice` title. This
example assumes there is a style token named `bold` in the custom style you are
using:
```python
Choice(
    title=[
        ('class:text', 'plain text '),
        ('class:bold', 'bold text')
    ]
)
```
As you can see it is possible to use custom style tokens for this purpose as
well. Note that Choices with token tuple titles will not be styled by the
`selected` or `highlighted` tokens. If not provided, the `value` of the Choice
will be the text concatenated (`'plain text bold text'` in the above example).
</details>

## How to Contribute

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

## Contributors

`questionary` is written and maintained by Tom Bocklisch.

It is based on the great work of [Oyetoke Toby](https://github.com/CITGuru/PyInquirer) 
as well as the work from [Mark Fink](https://github.com/finklabs/whaaaaat).

## Changelog

<details><summary>unreleased (master branch)</summary>

</details>

<details><summary>1.5.2 (16.04.2020)</summary>

Bug fix release.

* Added `.ask_async` support for forms.
</details>

<details><summary>1.5.1 (22.01.2020)</summary>

Bug fix release.

* Fixed `.ask_async` for questions on `prompt_toolkit==2.*`. Added tests for it.
</details>

<details><summary>1.5.0 (22.01.2020)</summary>

Feature release.

* Added support for prompt_toolkit 3
* All tests will be run against prompt_toolkit 2 and 3
* Removed support for python 3.5 (prompt_toolkit 3 does not support that anymore)
</details>

<details><summary>1.4.0 (10.11.2019)</summary>

Feature release.

* Added additional question type `autocomplete`
* Allow pointer and highlight in select question type
</details>

<details><summary>1.3.0 (25.08.2019)</summary>

Feature release.

* Add additional options to style checkboxes and select prompts https://github.com/tmbo/questionary/pull/14

</details>

<details><summary>1.2.1 (19.08.2019)</summary>

Bug fix release.

* Fixed compatibility with python 3.5.2 by removing `Type` annotation (this time for real)
</details>

<details><summary>1.2.0 (30.07.2019)</summary>

Feature release.

* Allow a user to pass in a validator as an instance https://github.com/tmbo/questionary/pull/10

</details>

<details><summary>1.1.1 (21.04.2019)</summary>

Bug fix release.

* Fixed compatibility with python 3.5.2 by removing `Type` annotation

</details>

<details><summary>1.1.0 (10.03.2019)</summary>

Feature release.

* Added `skip_if` to questions to allow skipping questions using a flag


</details>

<details><summary>1.0.2 (23.01.2019)</summary>

Bug fix release.

* Fixed odd behaviour if select is created without providing any choices
  instead, we will raise a `ValueError` now. ([#6](https://github.com/tmbo/questionary/pull/6))


</details>

<details><summary>1.0.1 (12.01.2019)</summary>

Bug fix release, adding some convenience shortcuts.

* Added shortcut keys `j` (move down^ the list) and `k` (move up) to
  the prompts `select` and `checkbox` (fixes [#2](https://github.com/tmbo/questionary/issues/2))
* Fixed unclosed file handle in `setup.py`
* Fixed unnecessary empty lines moving selections to far down (fixes [#3](https://github.com/tmbo/questionary/issues/3))

</details>

<details><summary>1.0.0 (14.12.2018)</summary>

Initial public release of the library

* Added python interface
* Added dict style question creation
* Improved the documentation
* More tests and automatic travis test execution
</details>

## Developer Info

<details>
<summary>Notes on how to do random things related to this repo</summary>

**Create one of the commandline recordings**

0. Install `brew install asciinema` and `npm install --global asciicast2gif`
1. Run `asciinema rec`
2. Do the thing
3. Convert to giv `asciicast2gif -h 7 -w 120 -s 2 <recoding> output.gif`

</details>

## License
Licensed under the MIT License. Copyright 2020 Tom Bocklisch. [Copy of the license](LICENSE).


[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Ftmbo%2Fquestionary?ref=badge_large)
