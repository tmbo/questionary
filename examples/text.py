# -*- coding: utf-8 -*-
"""Example for a list question type.

Run example by typing `python -m examples.input` in your console."""
import re
from pprint import pprint

from examples import custom_style_dope
from questionary import Validator, ValidationError, prompt


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = re.match(
            r'^([01])?[-.\s]?\(?(\d{3})\)?'
            r'[-.\s]?(\d{3})[-.\s]?(\d{4})\s?'
            r'((?:#|ext\.?\s?|x\.?\s?)(?:\d+)?)?$',
            document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


questions = [
    {
        'type': 'text',
        'name': 'first_name',
        'message': 'What\'s your first name',
    },
    {
        'type': 'text',
        'name': 'last_name',
        'message': 'What\'s your last name',
        'default': lambda a: 'Smith' if a['first_name'] == 'Dave' else 'Doe',
        'validate': lambda val: val == 'Doe' or 'is your last name Doe?'
    },
    {
        'type': 'text',
        'name': 'phone',
        'message': 'What\'s your phone number',
        'validate': PhoneNumberValidator
    }
]

if __name__ == '__main__':
    answers = prompt(questions, style=custom_style_dope)
    pprint(answers)
