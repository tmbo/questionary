# -*- coding: utf-8 -*-
"""Example for a select question type with search enabled.

Run example by typing `python -m examples.select_search` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import Choice
from questionary import Separator
from questionary import prompt


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.select(
        "What do you want to do?",
        qmark="😃",
        choices=[
            "Order a pizza",
            "Make a reservation",
            "Cancel a reservation",
            "Modify your order",
            Separator(),
            "Ask for opening hours",
            Choice("Contact support", disabled="Unavailable at this time"),
            "Talk to the receptionist",
        ],
        style=custom_style_dope,
        use_jk_keys=False,
        use_search_filter=True,
        **kwargs,
    )

    # prompt the user for an answer
    return question.ask()


def ask_dictstyle(**kwargs):
    questions = [
        {
            "type": "select",
            "name": "theme",
            "message": "What do you want to do?",
            "choices": [
                "Order a pizza",
                "Make a reservation",
                "Cancel a reservation",
                "Modify your order",
                Separator(),
                "Ask for opening hours",
                {"name": "Contact support", "disabled": "Unavailable at this time"},
                "Talk to the receptionist",
            ],
        }
    ]

    return prompt(questions, style=custom_style_dope, **kwargs)


if __name__ == "__main__":
    pprint(ask_pystyle())
