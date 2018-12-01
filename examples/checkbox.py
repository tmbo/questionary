# -*- coding: utf-8 -*-
"""
* Checkbox question example
* run example by typing `python example/checkbox.py` in your console
"""
from pprint import pprint

from examples import custom_style_dope
from questionary import prompt, Separator

questions = [
    {
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [
            {"name": "foo", "checked": True},
            Separator(),
            {"name": "bar", "disabled": "nope"},
            'bazz',
            Separator("--END--")]
    }
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_dope)
    pprint(answers)
