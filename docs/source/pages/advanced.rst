**************
Advanced Usage
**************

This section of the documentation describes some of the more advanced
uses of Questionary.

Validation
##########

Many of the promps support a :code:`validation` argument, which allows
the answer to be validated before being submitted.

The example below shows validation on a :meth:`~questionary.text` input:

.. code-block:: python3

  import questionary
  from questionary import Validator, ValidationError, prompt

  class NameValidator(Validator):
      def validate(self, document):
          if len(document.text) == 0:
              raise ValidationError(
                  message="Please enter a value",
                  cursor_position=len(document.text),
              )

  print(questionary.text("What's your name?", validate=NameValidator).ask())

Alternatively, we can replace the :code:`NameValidator` class with a simple
function, as seen below:

.. code-block:: python3

  import questionary

  print(questionary.text(
    "What's your name?",
    validate=lambda text: True if len(text) > 0 else "Please enter a value"
  ).ask())

Finally, if we do not care about the error message being displayed, we can ommit
the error message from the final example to use the default:

.. code-block:: python3

  import questionary

  print(questionary.text("What's your name?", validate=lambda text: len(text) > 0).ask())


Keyboard Interrupts
###################

Forms & Prompts
###############

Customising Text
################

Themes & Styling
################

You can customize all the colors used for the prompts. Every part of the prompt
has an identifier, which you can use to style it. Let's create our own custom style:

.. code-block:: python3

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

To use our custom style, we need to pass it to the question type:

.. code-block:: python3

  questionary.text("What's your phone number", style=custom_style_fancy).ask()

It is also possible to use a list of token tuples as a :code:`Choice` title.
This example assumes there is a style token named :code:`bold` in the custom
style that you are using:

.. code-block:: python3

  Choice(
      title=[
          ('class:text', 'plain text '),
          ('class:bold', 'bold text')
      ]
  )

As you can see, it is possible to use custom style tokens for this purpose as
well. Note that :code:`Choices` with token tuple titles will not be styled by
the :code:`selected` or :code:`highlighted` tokens. If not provided, the
:code:`value` of the :code:`Choice` will be the text concatenated
(:code:`'plain text bold text'` in the above example).

Prompts
#######

Text
****

Autocomplete
************

Checkbox & (Raw) Select
***********************

Choice and Separator

Path
****


Workflows
#########

Skipping Questions Using Conditions
***********************************

Sometimes it is helpful to be able to skip a question based on a condition.
To avoid the need for an :code:`if` around the question, you can pass the
condition when you create the question:

.. code-block:: python3

  DISABLED = True
  response = questionary.confirm("Are you amazed?").skip_if(DISABLED, default=True).ask()

If the condition (in this case :code:`DISABLED`) is :code:`True`, the question
will be skipped and the default value gets returned, otherwise the user will
be prompted as usual and the default value will be ignored.

Dictionary Configuration
************************

Instead of creating questions using the Python functions, you can also create them
using a configuration dictionary:

.. code-block:: python3

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

The returned :code:`answers` will be a dict containing the responses, e.g.
:code:`{"phone": "0123123", "continue": False, ""}`. The questions will be
prompted one after another and :code:`prompt` will return once all of them
are answered.

Each configuration dictionary needs to contain the following keys:

* :code:`type` - The type of the question.
* :code:`name` - The name of the question (will be used as key in the
  :code:`answers` dictionary).
* :code:`message` - Message that will be shown to the user.

Optional Keys:

* :code:`qmark` - Question mark to use - defaults to :code:`?`.
* :code:`default` - Preselected value.
* :code:`choices` - List of choices (applies when :code:`'type': 'select'`) or
  function returning a list of choices.

* :code:`when` - Function checking if this question should be shown or skipped
  (same functionality than :code:`.skip_if()`).

* :code:`validate` - Function or Validator Class performing validation (will
  be performed in real time as users type).

* :code:`filter` - Receive the user input and return the filtered value to be
  used inside the program. 

Further information can be found at the :class:`questionary.prompt`
documentation.

Example
*******
Questionary allows creating quite complex workflows when combining all of the
above concepts:

.. literalinclude:: ../../../examples/advanced_workflow.py
   :language: python3


The above workflow will show to the user the following prompts:

1. Yes/No question :code:`Would you like the next question?`.

2. :code:`Name this library?` - only shown when the first question is answered
   with yes.

3. A question to select an item from a list.
4. Free text inpt if :code:`'other'` is selected in step 3.

Depending on the route the user took, the result will look like the following:

.. code-block:: python3

  { 
      'conditional_step': False,
      'second_question': 'Testinput'   # Free form text
  }

.. code-block:: python3

  { 
      'conditional_step': True,
      'next_question': 'questionary',
      'second_question': 'Testinput'   # Free form text
  }

You can test this workflow yourself by running the
`advanced_workflow.py example <https://github.com/tmbo/questionary/blob/master/examples/advanced_workflow.py>`_.
