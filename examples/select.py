# -*- coding: utf-8 -*-
"""Example for a list question type.

Run example by typing `python -m examples.list` in your console."""
from pprint import pprint

from examples import custom_style_dope
from questionary import prompt, Separator


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers.get('size') == 'jumbo':
        options.append('helicopter')
    return options


questions = [
    {
        'type': 'select',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask for opening hours',
            {
                'name': 'Contact support',
                'disabled': 'Unavailable at this time'
            },
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'select',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower(),
        'when': lambda a: a['theme'] == 'Order a pizza'
    },
    {
        'type': 'select',
        'name': 'delivery',
        'message': 'Which vehicle you want to use for delivery?',
        'choices': get_delivery_options,
        'when': lambda a: a['theme'] == 'Order a pizza'
    },
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_dope)
    pprint(answers)
