# -*- coding: utf-8 -*-
"""Example for rawlist question type.

Run example by typing `python -m examples.rawlist` in your console."""
from pprint import pprint

from examples import custom_style_dope
from questionary import Separator, prompt

questions = [
    {
        'type': 'rawselect',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask opening hours',
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'rawselect',
        'name': 'size',
        'message': 'What size do you need',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    }
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_dope)
    pprint(answers)
