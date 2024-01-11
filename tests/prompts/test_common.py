from unittest.mock import Mock
from unittest.mock import call

import pytest
from prompt_toolkit.document import Document
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.styles import Attrs
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.validation import Validator

from questionary import Choice
from questionary.prompts import common
from questionary.prompts.common import InquirerControl
from questionary.prompts.common import build_validator
from questionary.prompts.common import print_formatted_text
from tests.utils import execute_with_input_pipe
from tests.utils import prompt_toolkit_version


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

    assert e.value.message == "Invalid input"


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

    def run(inp):
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

    execute_with_input_pipe(run)


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


def test_prompt_show_answer_with_shortcuts():
    ic = InquirerControl(
        ["a", Choice("b", shortcut_key=False), "c"],
        show_selected=True,
        use_shortcuts=True,
    )

    expected_tokens = [
        ("class:pointer", " » "),
        ("[SetCursorPosition]", ""),
        ("class:text", "○ "),
        ("class:highlighted", "1) a"),
        ("", "\n"),
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "-) b"),
        ("", "\n"),
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "2) c"),
        ("", "\n"),
        ("class:text", "  Answer: 1) a"),
    ]
    assert ic.pointed_at == 0
    assert ic._get_choice_tokens() == expected_tokens

    ic.select_next()
    expected_tokens = [
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "1) a"),
        ("", "\n"),
        ("class:pointer", " » "),
        ("[SetCursorPosition]", ""),
        ("class:text", "○ "),
        ("class:highlighted", "-) b"),
        ("", "\n"),
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "2) c"),
        ("", "\n"),
        ("class:text", "  Answer: -) b"),
    ]
    assert ic.pointed_at == 1
    assert ic._get_choice_tokens() == expected_tokens


def test_print(monkeypatch):
    mock = Mock(return_value=None)
    monkeypatch.setattr(DummyOutput, "write", mock)

    print_formatted_text("Hello World", output=DummyOutput())

    mock.assert_has_calls([call("Hello World"), call("\r\n")])


def test_print_with_style(monkeypatch):
    mock = Mock(return_value=None)
    monkeypatch.setattr(DummyOutput, "write", mock.write)
    monkeypatch.setattr(DummyOutput, "set_attributes", mock.set_attributes)

    print_formatted_text(
        "Hello World", style="bold italic fg:darkred", output=DummyOutput()
    )

    assert len(mock.method_calls) == 4
    assert mock.method_calls[0][0] == "set_attributes"

    if prompt_toolkit_version < (3, 0, 20):
        assert mock.method_calls[0][1][0] == Attrs(
            color="8b0000",
            bgcolor="",
            bold=True,
            underline=False,
            italic=True,
            blink=False,
            reverse=False,
            hidden=False,
        )
    else:
        assert mock.method_calls[0][1][0] == Attrs(
            color="8b0000",
            bgcolor="",
            bold=True,
            underline=False,
            italic=True,
            blink=False,
            reverse=False,
            hidden=False,
            strike=False,
        )

    assert mock.method_calls[1][0] == "write"
    assert mock.method_calls[1][1][0] == "Hello World"


def test_prompt_show_description():
    ic = InquirerControl(
        ["a", Choice("b", description="B")],
        show_selected=True,
        show_description=True,
    )

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
        ("class:text", "  Answer: a"),
    ]
    assert ic.pointed_at == 0
    assert ic._get_choice_tokens() == expected_tokens

    ic.select_next()
    expected_tokens = [
        ("class:text", "   "),
        ("class:text", "○ "),
        ("class:text", "a"),
        ("", "\n"),
        ("class:pointer", " » "),
        ("[SetCursorPosition]", ""),
        ("class:text", "○ "),
        ("class:highlighted", "b"),
        ("", "\n"),
        ("class:text", "  Answer: b"),
        ("class:text", "  Description: B"),
    ]
    assert ic.pointed_at == 1
    assert ic._get_choice_tokens() == expected_tokens
