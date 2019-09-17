from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from pytest import fail

import questionary
from questionary import form, Choice
from tests.utils import KeyInputs


def example_form(inp):
    return form(q1=questionary.confirm("Hello?",
                                       input=inp,
                                       output=DummyOutput()),
                q2=questionary.select("World?",
                                      choices=["foo", "bar"],
                                      input=inp,
                                      output=DummyOutput(),
                                      default='default'
                                      )).skip_if(q2=lambda x: not x['q1'])


def test_form_creation():
    inp = create_pipe_input()
    text = "Y" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = example_form(inp)

        result = f.unsafe_ask()

        assert result == {'q1': True, 'q2': 'foo'}
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


def test_select_skip_on_condition():
    inp = create_pipe_input()
    text = "N" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = example_form(inp)

        result = f.unsafe_ask()

        assert result == {'q1': False, 'q2': 'default'}
    finally:
        inp.close()


def test_checkbox_default_on_condition():
    inp = create_pipe_input()
    text = "N" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = form(q1=questionary.confirm("Hello?",
                                        input=inp,
                                        output=DummyOutput()),
                 q2=questionary.checkbox("World?",
                                         choices=["foo", "bar"],
                                         input=inp,
                                         output=DummyOutput(),
                                         default='default'
                                         )).skip_if(q2=lambda x: not x['q1'])

        result = f.unsafe_ask()

        assert result == {'q1': False, 'q2': 'default'}
    finally:
        inp.close()


def test_checkbox_checked_default_on_condition():
    inp = create_pipe_input()
    text = "N" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        f = form(q1=questionary.confirm("Hello?",
                                        input=inp,
                                        output=DummyOutput()),
                 q2=questionary.checkbox("World?",
                                         choices=[
                                             Choice("foo", checked=True),
                                             "bar"
                                         ],
                                         input=inp,
                                         output=DummyOutput(),
                                         )).skip_if(q2=lambda x: not x['q1'])

        result = f.unsafe_ask()

        assert result == {'q1': False, 'q2': ("foo",)}
    finally:
        inp.close()
