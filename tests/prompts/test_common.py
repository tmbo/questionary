import pytest
from prompt_toolkit.document import Document
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.validation import ValidationError, Validator
from questionary.prompts import common

from questionary.prompts.common import InquirerControl, build_validator


def test_to_many_choices_for_shortcut_assignment():
    ic = InquirerControl([str(i) for i in range(1, 100)], use_shortcuts=True)

    # IC should fail gracefully when running out of shortcuts
    assert len(list(filter(lambda x: x.shortcut_key is not None, ic.choices))) == len(
        InquirerControl.SHORTCUT_KEYS
    )


def test_validator_bool_function():
    def validate(t):
        return len(t) == 3

    validator = build_validator(validate)
    assert validator.validate(Document("foo")) is None  # should not raise


def test_validator_bool_function_fails():
    def validate(t):
        return len(t) == 3

    validator = build_validator(validate)
    with pytest.raises(ValidationError) as e:
        validator.validate(Document("fooooo"))

    assert e.value.message == "invalid input"


def test_validator_instance():
    def validate(t):
        return len(t) == 3

    validator = Validator.from_callable(validate)

    validator = build_validator(validator)
    assert validator.validate(Document("foo")) is None  # should not raise


def test_validator_instance_fails():
    def validate(t):
        return len(t) == 3

    validator = Validator.from_callable(validate, error_message="invalid input")
    with pytest.raises(ValidationError) as e:
        validator.validate(Document("fooooo"))

    assert e.value.message == "invalid input"


def test_blank_line_fix():
    def get_prompt_tokens():
        return [("class:question", "What is your favourite letter?")]

    ic = InquirerControl(["a", "b", "c"])

    inp = create_pipe_input()

    try:
        inp.send_text("")
        layout = common.create_inquirer_layout(
            ic, get_prompt_tokens, input=inp, output=DummyOutput()
        )

        # usually this would be 2000000000000000000000000000000
        # but `common._fix_unecessary_blank_lines` makes sure
        # the main window is not as greedy (avoiding blank lines)
        assert (
            layout.container.preferred_height(100, 200).max
            == 1000000000000000000000000000001
        )
    finally:
        inp.close()


def test_prompt_highlight_coexist():
    ic = InquirerControl(["a", "b", "c"])

    expected_tokens = [
        ("class:pointer", " » "),
        ("[SetCursorPosition]", ""),
        ("class:text", "○ "),
        ("class:highlighted", "a"),
        ("", "\n"),
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "b"),
        ("", "\n"),
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "c"),
    ]
    assert ic.pointed_at == 0
    assert ic._get_choice_tokens() == expected_tokens

    ic.select_previous()
    expected_tokens = [
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "a"),
        ("", "\n"),
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "b"),
        ("", "\n"),
        ("class:pointer", " » "),
        ("[SetCursorPosition]", ""),
        ("class:text", "○ "),
        ("class:highlighted", "c"),
    ]
    assert ic.pointed_at == 2
    assert ic._get_choice_tokens() == expected_tokens
