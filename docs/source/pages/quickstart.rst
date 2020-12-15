**********
Quickstart
**********

Here are some quick examples of all the inputs.

## Text

A free text input for the user.

```python
questionary.text("What's your first name").ask()
```
![example-gif](../../images/text.gif)

## Password

A free text input for the user where the input is not
shown but replaced with `***`.

```python
questionary.password("What's your secret?").ask()
```

![example-gif](../../images/password.gif)

## File Path

A text input for a file or directory path with autocompletion enabled.

```python
questionary.path("Path to the projects version file").ask()
```

![example-gif](../../images/path.gif)

## Confirmation

A yes or no question. The user can either confirm or deny.

```python
questionary.confirm("Are you amazed?").ask()
```

![example-gif](../../images/confirm.gif)

## Select

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

![example-gif](../../images/select.gif)

## Raw Select

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

![example-gif](../../images/rawselect.gif)

## Checkbox

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
![example-gif](../../images/checkbox.gif)

## Autocomplete

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
![example-gif](../../images/autocomplete.gif)


## Printing Formatted Text

Sometimes you want to spice up your printed messages a bit, `questionary.print`
is a helper to do just that:

```python
questionary.print("Hello World 🦄", style="bold italic fg:darkred")
```
![example-gif](../../images/print.gif) 

The style argument uses the prompt [toolkit style strings].

[toolkit style strings]: https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/styling.html#style-strings
