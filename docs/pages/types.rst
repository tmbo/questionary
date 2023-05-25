.. _question_types:

**************
Question Types
**************

The different question types are meant to cover different use cases. The
parameters and configuration options are explained in detail for each
type. But before we get into to many details, here is a **cheatsheet
with the available question types**:

* use :ref:`type_text` to ask for **free text** input

* use :ref:`type_password` to ask for free text where the **text is hidden**

* use :ref:`type_path` to ask for a **file or directory** path with autocompletion

* use :ref:`type_confirm` to ask a **yes or no** question

* use :ref:`type_select` to ask the user to select **one item** from a beautiful list

* use :ref:`type_raw_select` to ask the user to select **one item** from a list

* use :ref:`type_checkbox` to ask the user to select **any number of items** from a list

* use :ref:`type_autocomplete` to ask for free text with **autocomplete help**

* use :ref:`type_press_any_key_to_continue` to ask the user to **press any key to continue**

.. _type_text:

Text
####

.. automethod:: questionary::text

.. _type_password:

Password
########

.. automethod:: questionary::password

.. _type_path:

File Path
#########

.. automethod:: questionary::path

.. _type_confirm:

Confirmation
############

.. automethod:: questionary::confirm

.. _type_select:

Select
######

.. automethod:: questionary::select

.. _type_raw_select:

Raw Select
##########

.. automethod:: questionary::rawselect

.. _type_checkbox:

Checkbox
########

.. automethod:: questionary::checkbox

.. _type_autocomplete:

Autocomplete
############

.. automethod:: questionary::autocomplete

Printing Formatted Text
#######################

.. automethod:: questionary::print

.. _type_press_any_key_to_continue:

Press Any Key To Continue
#########################

.. automethod:: questionary::press_any_key_to_continue
