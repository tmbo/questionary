# -*- coding: utf-8 -*-
"""Example for a checkbox question type.

Run example by typing `python -m examples.checkbox` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import Separator, Choice

question = questionary.checkbox(
    'Select toppings',
    qmark='😃',
    choices=[
        Choice("foo", is_initially_selected=True),
        Separator(),
        Choice("bar", disabled="nope"),
        'bazz',
        Separator("--END--")],
    style=custom_style_dope)

if __name__ == '__main__':
    answers = question.ask()
    pprint(answers)
