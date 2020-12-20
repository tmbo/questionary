.. _question_types:

**************
Question Types
**************

The different question types are meant to cover different use cases. The
parameters and configuration options are explained in detail for each
type. But before we get into to many details, here is a **cheatsheet
with the available question types**:

* use :ref:`type_text` to ask for **free text** input

  .. code-block:: python3

    questionary.text("What's your first name?").ask()

* use :ref:`type_password` to ask for free text where the **text is hidden**


  .. code-block:: python3

    questionary.password("What's your secret?").ask()

* use :ref:`type_path` to ask for a **file or directory** path with autocompletion


  .. code-block:: python3

    questionary.path("What's the path to the projects version file?").ask()

* use :ref:`type_confirm` to ask a **yes or no** question


  .. code-block:: python3

    questionary.confirm("Are you amazed?").ask()

* use :ref:`type_select` to ask the user to select **one item** from a beautiful list

  .. code-block:: python3

    questionary.select(
        "What do you want to do?",
        choices=[
            "Order a pizza",
            "Make a reservation",
            "Ask for opening hours"
        ]).ask()

* use :ref:`type_raw_select` to ask the user to select **one item** from a list

  .. code-block:: python3

    questionary.rawselect(
        "What do you want to do?",
        choices=[
            "Order a pizza",
            "Make a reservation",
            "Ask for opening hours"
        ]).ask()

* use :ref:`type_checkbox` to ask the user to select **any number of items** from a list

  .. code-block:: python3

    questionary.checkbox(
        'Select toppings',
        choices=[
            "Cheese",
            "Tomato",
            "Pineapple"
        ]).ask()


* use :ref:`type_autocomplete` to ask for free text with **autocomplete help**

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

.. _type_text:

Text
####

A free text input for the user.

.. code-block:: python3

  questionary.text("What's your first name").ask()

.. image:: ../images/text.gif

.. module:: questionary

.. automethod:: questionary.text

.. _type_password:

Password
########

A free text input for the user where the input is not
shown but replaced with `***`.

.. code-block:: python3

  questionary.password("What's your secret?").ask()

.. image:: ../images/password.gif

.. _type_path:

File Path
#########

A text input for a file or directory path with autocompletion enabled.

.. code-block:: python3

  questionary.path("What's the path to the projects version file?").ask()

.. image:: ../images/path.gif

.. _type_confirm:

Confirmation
############

A yes or no question. The user can either confirm or deny.

.. code-block:: python3

  questionary.confirm("Are you amazed?").ask()

.. image:: ../images/confirm.gif

.. _type_select:

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

.. image:: ../images/select.gif

.. _type_raw_select:

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

.. image:: ../images/rawselect.gif

.. _type_checkbox:

Checkbox
########

A list of items to select multiple choices from. The user can pick
none, one or multiple options and confirm the selection.

.. code-block:: python3

  questionary.checkbox(
     'Select toppings',
     choices=[
         "Cheese",
         "Tomato",
         "Pineapple",
     ]).ask()

.. image:: ../images/checkbox.gif

.. _type_autocomplete:

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

.. image:: ../images/autocomplete.gif

Printing Formatted Text
#######################

Sometimes you want to spice up your printed messages a bit, `questionary.print`
is a helper to do just that:

.. code-block:: python3

  questionary.print("Hello World 🦄", style="bold italic fg:darkred")

.. image:: ../images/print.gif

The style argument uses the prompt :ref:`toolkit style strings <prompt_toolkit:styling>`.
