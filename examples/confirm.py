# -*- coding: utf-8 -*-
"""
* Confirm question example
* run example by typing `python example/confirm.py` in your console
"""
from __future__ import print_function

from pprint import pprint

from questionary import prompt
from examples import custom_style_fancy

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

answers = prompt(questions, style=custom_style_fancy)
pprint(answers)
