# Advanced Usage

## Validation

## Workflows

### Skipping Questions Using Conditions

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

### Dictionary Configuration

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

### Example
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

## Themes and Styling

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
