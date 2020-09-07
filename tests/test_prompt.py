import pytest

from questionary.prompt import PromptParameterException, prompt


def test_missing_message():
    with pytest.raises(PromptParameterException):
        prompt([{"type": "confirm", "name": "continue", "default": True}])


def test_missing_type():
    with pytest.raises(PromptParameterException):
        prompt(
            [
                {
                    "message": "Do you want to continue?",
                    "name": "continue",
                    "default": True,
                }
            ]
        )


def test_missing_name():
    with pytest.raises(PromptParameterException):
        prompt(
            [
                {
                    "type": "confirm",
                    "message": "Do you want to continue?",
                    "default": True,
                }
            ]
        )


def test_invalid_question_type():
    with pytest.raises(ValueError):
        prompt(
            [
                {
                    "type": "mytype",
                    "message": "Do you want to continue?",
                    "name": "continue",
                    "default": True,
                }
            ]
        )
