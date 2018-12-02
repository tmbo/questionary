# -*- coding: utf-8 -*-
"""Example for a confirm question type.

Run example by typing `python -m examples.confirm` in your console."""
from pprint import pprint

from examples import custom_style_fancy
from questionary import prompt

questions = [
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    },
    {
        'type': 'confirm',
        'message': "Do you want to exit? Oh, I haven't actually experience "
                   "that. I'll look into it. Under your repository name, "
                   "click Pull requests. Under your repository name, "
                   "click Pull requests.",
        'name': 'exit',
        'default': False,
    },
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_fancy)
    pprint(answers)
