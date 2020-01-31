# -*- coding: utf-8 -*-
"""Example for a text question type.

Run example by typing `python -m examples.text` in your console."""
import re
from pprint import pprint

import questionary
from examples import custom_style_dope
from questionary import Validator, ValidationError, prompt


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = re.match(
            r"^([01])?[-.\s]?\(?(\d{3})\)?"
            r"[-.\s]?(\d{3})[-.\s]?(\d{4})\s?"
            r"((?:#|ext\.?\s?|x\.?\s?)(?:\d+)?)?$",
            document.text,
        )
        if not ok:
            raise ValidationError(
                message="Please enter a valid phone number",
                cursor_position=len(document.text),
            )  # Move cursor to end


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.text(
        "What's your phone number",
        validate=PhoneNumberValidator,
        style=custom_style_dope,
        **kwargs,
    )

    # prompt the user for an answer
    return question.ask()


def ask_dictstyle(**kwargs):
    questions = [
        {
            "type": "text",
            "name": "phone",
            "message": "What's your phone number",
            "validate": PhoneNumberValidator,
        }
    ]

    return prompt(questions, style=custom_style_dope, **kwargs)


if __name__ == "__main__":
    pprint(ask_pystyle())
