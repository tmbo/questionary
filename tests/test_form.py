from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from pytest import fail

import questionary
from questionary import form
from tests.utils import KeyInputs


def example_form(inp):
    return form(
        q1=questionary.confirm("Hello?", input=inp, output=DummyOutput()),
        q2=questionary.select(
            "World?", choices=["foo", "bar"], input=inp, output=DummyOutput()
        ),
    )


def example_form_with_skip(inp):
    return form(
        q1=questionary.confirm("Hello?", input=inp, output=DummyOutput()),
        q2=questionary.select(
            "World?", choices=["foo", "bar"], input=inp, output=DummyOutput()
        ).skip_if(True, 42),
    )


def test_form_creation():
    inp = create_pipe_input()
    text = "Y" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = example_form(inp)

        result = f.unsafe_ask()

        assert result == {"q1": True, "q2": "foo"}
    finally:
        inp.close()


def test_form_skips_questions():
    inp = create_pipe_input()
    text = "Y" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = example_form_with_skip(inp)

        result = f.ask()

        assert result == {"q1": True, "q2": 42}
    finally:
        inp.close()


def test_form_skips_questions_unsafe_ask():
    inp = create_pipe_input()
    text = "Y" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = example_form_with_skip(inp)

        result = f.unsafe_ask()

        assert result == {"q1": True, "q2": 42}
    finally:
        inp.close()


def test_ask_should_catch_keyboard_exception():
    inp = create_pipe_input()

    try:
        inp.send_text(KeyInputs.CONTROLC)
        f = example_form(inp)

        result = f.ask()
        assert result == {}
    except KeyboardInterrupt:
        fail("Keyboard Interrupt should be caught by `ask()`")
    finally:
        inp.close()
