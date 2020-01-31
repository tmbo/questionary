# -*- coding: utf-8 -*-
"""Example for a confirm question type.

Run example by typing `python -m examples.confirm` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import prompt


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.confirm(
        "Do you want to continue?", default=True, style=custom_style_dope, **kwargs
    )

    # prompt the user for an answer
    return question.ask()


def ask_dictstyle(**kwargs):
    questions = [
        {
            "type": "confirm",
            "message": "Do you want to continue?",
            "name": "continue",
            "default": True,
        }
    ]

    return prompt(questions, style=custom_style_dope, **kwargs)


if __name__ == "__main__":
    pprint(ask_pystyle())
