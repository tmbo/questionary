# -*- coding: utf-8 -*-
"""
* password question example
"""
from __future__ import print_function, unicode_literals

from pprint import pprint

from questionary import prompt
from examples import custom_style_dope

questions = [
    {
        'type': 'password',
        'message': 'Enter your git password',
        'name': 'password'
    }
]

answers = prompt(questions, style=custom_style_dope)
pprint(answers)
