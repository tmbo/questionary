from pprint import pprint

from questionary import Separator
from questionary import prompt


def ask_dictstyle(**kwargs):
    questions = [
        {
            # just print a message, don't ask a question
            # does not require a name (but if provided, is ignored) and does not return a value
            "type": "print",
            "name": "intro",
            "message": "This example demonstrates advanced features! 🦄",
            "style": "bold italic",
        },
        {
            "type": "confirm",
            "name": "conditional_step",
            "message": "Would you like the next question?",
            "default": True,
        },
        {
            "type": "text",
            "name": "next_question",
            "message": "Name this library?",
            # Validate if the first question was answered with yes or no
            "when": lambda x: x["conditional_step"],
            # Only accept questionary as answer
            "validate": lambda val: val == "questionary",
        },
        {
            "type": "select",
            "name": "second_question",
            "message": "Select item",
            "choices": ["item1", "item2", Separator(), "other"],
        },
        {
            # just print a message, don't ask a question
            # does not require a name and does not return a value
            "type": "print",
            "message": "Please enter a value for 'other'",
            "style": "bold italic fg:darkred",
            "when": lambda x: x["second_question"] == "other",
        },
        {
            "type": "text",
            # intentionally overwrites result from previous question
            "name": "second_question",
            "message": "Insert free text",
            "when": lambda x: x["second_question"] == "other",
        },
    ]
    return prompt(questions, **kwargs)


if __name__ == "__main__":
    pprint(ask_dictstyle())
