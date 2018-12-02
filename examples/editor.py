# -*- coding: utf-8 -*-
"""Example for a editor question type.

Run example by typing `python -m examples.editor` in your console."""
from pprint import pprint

from examples import custom_style_dope
from questionary import prompt

questions = [
    {
        'type': 'editor',
        'name': 'bio',
        'message': 'Please write a short bio of at least 3 lines.',
        'default': 'Hello World',
        'validate': lambda text: (len(text.split('\n')) >= 3 or
                                  'Must be at least 3 lines.'),
        'eargs': {
            'editor': 'default',
            'ext': '.py'
        }
    }
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_dope)
    pprint(answers)
