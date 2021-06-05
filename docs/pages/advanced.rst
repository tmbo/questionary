*****************
Advanced Concepts
*****************

This page describes some of the more advanced uses of Questionary.

Validation
##########

Many of the prompts support a ``validate`` argument, which allows
the answer to be validated before being submitted. A user can not
submit an answer if it doesn't pass the validation.

The example below shows :meth:`~questionary.text` input with
a validation:

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

  questionary.text("What's your name?", validate=NameValidator).ask()

In this example, the user can not enter a non empty value. If the
prompt is submitted without a value. Questionary will show the error
message and reject the submission until the user enters a value.

Alternatively, we can replace the ``NameValidator`` class with a simple
function, as seen below:

.. code-block:: python3

  import questionary

  print(questionary.text(
    "What's your name?",
    validate=lambda text: True if len(text) > 0 else "Please enter a value"
  ).ask())

Finally, if we do not care about the error message being displayed, we can omit
the error message from the final example to use the default:

.. code-block:: python3

  import questionary

  print(questionary.text("What's your name?", validate=lambda text: len(text) > 0).ask())

.. admonition:: example
  :class: info

  The :meth:`~questionary.checkbox` prompt does not support passing a
  ``Validator``. See the :ref:`API Reference <api-reference>` for all the prompts which
  support the ``validate`` parameter.

A Validation Example using the Password Question
************************************************

Here we see an example of ``validate`` being used on a
:meth:`~questionary.password` prompt to enforce complexity requirements:

.. code-block:: python3

  import re
  import questionary

  def password_validator(password):

      if len(password) < 10:
          return "Password must be at least 10 characters"

      elif re.search("[0-9]", password) is None:
          return "Password must contain a number"

      elif re.search("[a-z]", password) is None:
          return "Password must contain an lower-case letter"

      elif re.search("[A-Z]", password) is None:
          return "Password must contain an upper-case letter"

      else:
          return True

  print(questionary.password("Enter your password", validate=password_validator).ask())

Keyboard Interrupts
###################

Prompts can be invoked in either a 'safe' or 'unsafe' way. The safe way
captures keyboard interrupts and handles them by catching the interrupt
and returning ``None`` for the asked question. If a question is asked
using unsafe functions, the keyboard interrupts are not caught.

Safe
****

The following are safe (capture keyboard interrupts):

* :meth:`~questionary.prompt`;

* :attr:`~questionary.Form.ask` on :class:`~questionary.Form` (returned by
  :meth:`~questionary.form`);

* :attr:`~questionary.Question.ask` on :class:`~questionary.Question`, which
  is returned by the various prompt functions (e.g. :meth:`~questionary.text`,
  :meth:`~questionary.checkbox`).

When a keyboard interrupt is captured, the message ``"Cancelled by user"`` is
displayed (or a custom message, if one is given) and ``None`` is returned.
Here is an example:

.. code:: python3

    # Questionary handles keyboard interrupt and returns `None` if the
    # user hits e.g. `Ctrl+C`
    prompt(...)

Unsafe
******

The following are unsafe (do not catch keyboard interrupts):

* :meth:`~questionary.unsafe_prompt`;

* :attr:`~questionary.Form.unsafe_ask` on :class:`~questionary.Form` (returned by
  :meth:`~questionary.form`);

* :attr:`~questionary.Question.unsafe_ask` on :class:`~questionary.Question`,
  which is returned by the various prompt functions (e.g. :meth:`~questionary.text`,
  :meth:`~questionary.checkbox`).
  
As a caller you must handle keyboard interrupts yourself
when calling these methods. Here is an example:

.. code:: python3

    try:
        unsafe_prompt(...)

    except KeyboardInterrupt:
        # your chance to handle the keyboard interrupt
        print("Cancelled by user")


Asynchronous Usage
##################

If you are running asynchronous code and you want to avoid blocking your
async loop, you can ask your questions using ``await``.
:class:`questionary.Question` and :class:`questionary.Form` have
``ask_async`` and ``unsafe_ask_async`` methods to invoke the
question using :mod:`python:asyncio`:

.. code-block:: python3

  import questionary

  answer = await questionary.text("What's your name?").ask_async()

Themes & Styling
################

You can customize all the colors used for the prompts. Every part of the prompt
has an identifier, which you can use to style it. Let's create your own custom
style:

.. code-block:: python3

  from questionary import Style

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

To use the custom style, you need to pass it to the question as a parameter:

.. code-block:: python3

  questionary.text("What's your phone number", style=custom_style_fancy).ask()

.. note::

  Default values will be used for any token types not specified in your custom style.

Styling Choices in Select & Checkbox Questions
**********************************************

It is also possible to use a list of token tuples as a ``Choice`` title to
change how an option is displayed in :class:`questionary.select` and
:class:`questionary.checkbox`. Make sure to define any additional styles
as part of your custom style definition.

.. code-block:: python3

  import questionary
  from questionary import Choice, Style

  custom_style_fancy = questionary.Style([
      ("highlighted", "bold"),  # style for a token which should appear highlighted
  ])

  choices = [Choice(title=[("class:text", "order a "),
                           ("class:highlighted", "big pizza")])]

  questionary.select(
     "What do you want to do?",
     choices=choices,
     style=custom_style_fancy).ask()

Conditionally Skip Questions
############################

Sometimes it is helpful to be able to skip a question based on a condition.
To avoid the need for an ``if`` around the question, you can pass the
condition when you create the question:

.. code-block:: python3

  import questionary

  DISABLED = True
  response = questionary.confirm("Are you amazed?").skip_if(DISABLED, default=True).ask()

If the condition (in this case ``DISABLED``) is ``True``, the question
will be skipped and the default value gets returned, otherwise the user will
be prompted as usual and the default value will be ignored.

.. _question_dictionaries:

Create Questions from Dictionaries
##################################

Instead of creating questions using the Python functions, you can also create
them using a configuration dictionary:

.. code-block:: python3

  from questionary import prompt

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

The questions will be prompted one after another and ``prompt`` will return
as soon as all of them are answered. The returned ``answers``
will be a dictionary containing the responses, e.g.

.. code-block:: python3

  {"phone": "0123123", "continue": False}.

Each configuration dictionary for a question must contain the
following keys:

``type`` (required)
   The type of the question.

``name`` (required)
  The name of the question (will be used as key in the
  ``answers`` dictionary).

``message`` (required)
  Message that will be shown to the user.

In addition to these required configuration parameters, you can
add the following optional parameters:

``qmark`` (optional)
  Question mark to use - defaults to ``?``.

``default`` (optional)
  Preselected value.

``choices`` (optional)
  List of choices (applies when ``'type': 'select'``)
  or function returning a list of choices.

``when`` (optional)
  Function checking if this question should be shown
  or skipped (same functionality as :attr:`~questionary.Question.skip_if`).

``validate`` (optional)
  Function or Validator Class performing validation (will
  be performed in real time as users type).

``filter`` (optional)
  Receive the user input and return the filtered value to be
  used inside the program. 

Further information can be found at the :class:`questionary.prompt`
documentation.

.. _random_label:

A Complex Example using a Dictionary Configuration
**************************************************

Questionary allows creating quite complex workflows when combining all of the
above concepts:

.. literalinclude:: ../../examples/advanced_workflow.py
   :language: python3


The above workflow will show to the user the following prompts:

1. Yes/No question ``"Would you like the next question?"``.

2. ``"Name this library?"`` - only shown when the first question is answered
   with yes.

3. A question to select an item from a list.
4. Free text input if ``"other"`` is selected in step 3.

Depending on the route the user took, the result will look like the following:

.. code-block:: python3

  { 
      'conditional_step': False,
      'second_question': 'Test input'   # Free form text
  }

.. code-block:: python3

  { 
      'conditional_step': True,
      'next_question': 'questionary',
      'second_question': 'Test input'   # Free form text
  }

You can test this workflow yourself by running the
`advanced_workflow.py example <https://github.com/tmbo/questionary/blob/master/examples/advanced_workflow.py>`_.
