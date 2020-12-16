# -*- coding: utf-8 -*-
"""Example for a checkbox question type.

Run example by typing `python -m examples.checkbox` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import Separator, Choice, prompt


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.checkbox(
        "Select toppings",
        # Add a validator.
        validate=lambda a: (len(a) >= 3, "You must select at least three toppings"),
        # Change the question mark symbol.
        qmark="😃",
        choices=[
            # These two options are checked by default.
            Choice("Cheese", checked=True),
            Choice("Tomatoe", checked=True),
            Choice("Peppers"),
            # Here we add a separator.
            Separator("--Premium--"),
            # This option is disabled.
            Choice("Salami", disabled="Out of Stock"),
            Choice("Pepperoni"),
        ],
    )
    # prompt the user for an answer
    return question.ask()


def ask_dictstyle(**kwargs):
    questions = [
        {
            "type": "checkbox",
            "qmark": "😃",
            "message": "Select toppings",
            "name": "toppings",
            "choices": [
                {"name": "foo", "checked": True},
                Separator(),
                {"name": "bar", "disabled": "nope"},
                "bazz",
                Separator("--END--"),
            ],
        }
    ]

    return prompt(questions, style=custom_style_dope, **kwargs)


if __name__ == "__main__":
    pprint(ask_pystyle())
