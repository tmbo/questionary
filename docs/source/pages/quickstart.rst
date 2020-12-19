**********
Quickstart
**********

Here are some quick examples of all the inputs.

Text
####

A free text input for the user.

.. code-block:: python3

  questionary.text("What's your first name").ask()

.. image:: ../../images/text.gif

Password
########

A free text input for the user where the input is not
shown but replaced with `***`.

.. code-block:: python3

  questionary.password("What's your secret?").ask()

.. image:: ../../images/password.gif

File Path
#########

A text input for a file or directory path with autocompletion enabled.

.. code-block:: python3

  questionary.path("Path to the projects version file").ask()

.. image:: ../../images/path.gif

Confirmation
############

A yes or no question. The user can either confirm or deny.

.. code-block:: python3

  questionary.confirm("Are you amazed?").ask()

.. image:: ../../images/confirm.gif

Select
######

A list of items to select a choice from. The user can pick
one option and confirm it.

.. code-block:: python3

  questionary.select(
     "What do you want to do?",
     choices=[
         "Order a pizza",
         "Make a reservation",
         "Ask for opening hours"
     ]).ask()

.. image:: ../../images/select.gif

Raw Select
##########

A list of items to select a choice from. The user can pick
one option using shortcuts and confirm it.

.. code-block:: python3

  questionary.rawselect(
     "What do you want to do?",
     choices=[
         "Order a pizza",
         "Make a reservation",
         "Ask for opening hours"
     ]).ask()

.. image:: ../../images/rawselect.gif

Checkbox
########

A list of items to select multiple choices from. The user can pick
none, one or multiple options and confirm the selection.

.. code-block:: python3

  questionary.checkbox(
     'Select toppings',
     choices=[
         "foo",
         "bar",
         "bazz"
     ]).ask()

.. image:: ../../images/checkbox.gif

Autocomplete
############

Text input with autocomplete help.

.. code-block:: python3

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

.. image:: ../../images/autocomplete.gif

Printing Formatted Text
#######################

Sometimes you want to spice up your printed messages a bit, `questionary.print`
is a helper to do just that:

.. code-block:: python3

  questionary.print("Hello World 🦄", style="bold italic fg:darkred")

.. image:: ../../images/print.gif

The style argument uses the prompt :ref:`toolkit style strings <prompt_toolkit:styling>`.
