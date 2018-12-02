# -*- coding: utf-8 -*-
"""Example for a password question type.

Run example by typing `python -m examples.password` in your console."""
from pprint import pprint

from examples import custom_style_dope
from questionary import prompt

questions = [
    {
        'type': 'password',
        'message': 'Enter your git password',
        'name': 'password'
    }
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_dope)
    pprint(answers)
