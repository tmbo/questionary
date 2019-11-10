# -*- coding: utf-8 -*-
"""Example for a password question type.

Run example by typing `python -m examples.password` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import Separator, Choice, prompt


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.password(
        "Enter your git password", style=custom_style_dope, **kwargs
    )

    # prompt the user for an answer
    return question.ask()


def ask_dictstyle(**kwargs):
    questions = [
        {"type": "password", "message": "Enter your git password", "name": "password"}
    ]

    return prompt(questions, style=custom_style_dope, **kwargs)


if __name__ == "__main__":
    pprint(ask_pystyle())
