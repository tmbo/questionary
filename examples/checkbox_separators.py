# -*- coding: utf-8 -*-
"""Example for a checkbox question type.

Run example by typing `python -m examples.checkbox` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import Choice
from questionary import Separator
from questionary import prompt


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.checkbox(
        "Select toppings",
        qmark="😃",
        choices=[
            Choice("foo", checked=True),
            Separator(),
            Choice("bar", disabled="nope"),
            "bazz",
            Separator("--END--"),
        ],
        style=custom_style_dope,
        **kwargs,
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
