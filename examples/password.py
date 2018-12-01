# -*- coding: utf-8 -*-
"""
* password question example
"""
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

answers = prompt(questions, style=custom_style_dope)
pprint(answers)
