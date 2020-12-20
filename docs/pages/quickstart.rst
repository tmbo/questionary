.. _quickstart:

**********
Quickstart
**********

Questionary supports two different concepts:

- creating a **single question** for the user

  .. code-block:: python3

        questionary.password("What's your secret?").ask()

- creating a **form with multiple questions** asked one after another

  .. code-block:: python3

      answers = questionary.form(
          first = questionary.confirm("Would you like the next question?", default=True),
          second = questionary.select("Select item", choices=["item1", "item2", "item3"])
      ).ask()

Asking a Single Question
========================

Questionary ships with a lot of different :ref:`question_types` to provide
the right prompt for the right question. All of them work in the same way though.
Firstly, you create a question:

.. code:: python3

  import questionary

  question = questionary.text("What's your first name")

and secondly, you need to prompt the user to answer it:

.. code:: python3

  answer = question.ask()

Since our question is a ``text`` prompt, ``answer`` will
contain the text the user typed after they submitted it.

You can concatenate creating and asking the question in a single
line if you like, e.g.

.. code:: python3

  import questionary

  answer = questionary.text("What's your first name").ask()

.. note::

  There are a lot more question types apart from  ``text``.
  For a description of the different question types, head
  over to the :ref:`question_types`.

Asking Multiple Questions
=========================

You can use the :meth:`~questionary.form` function to ask a collection
of :class:`Questions <questionary.Question>`. The questions will be asked in
the order they are passed to `:meth:`~questionary.form``.

.. code:: python3

  import questionary

  answers = questionary.form(
      first = questionary.confirm("Would you like the next question?", default=True),
      second = questionary.select("Select item", choices=["item1", "item2", "item3"])
  ).ask()

  print(answers)

The printed output will have the following format:

.. code-block:: python3

  {'first': True, 'second': 'item2'}

The :meth:`~questionary.prompt` function also allows you to ask a
collection of questions, however instead of taking :class:`~questionary.Question`
instances, it takes a dictionary:

.. code:: python3

  import questionary

  questions = [
    {
      "type": "confirm",
      "name": "first",
      "message": "Would you like the next question?",
      "default": True,
    },
    {
      "type": "select",
      "name": "second",
      "message": "Select item",
      "choices": ["item1", "item2", "item3"],
    },
  ]

  questionary.prompt(questions)

The format of the returned answers is the same as the one for
:meth:`~questionary.form`. You can find more details on the configuration
dictionaries in :ref:`question_dictionaries`.
