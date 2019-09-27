import pytest
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from pytest import fail

import questionary
from questionary import form, Choice
from questionary.form import DependencyError
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
                 q2=questionary.select("World?",
                                       choices=["foo", "bar"],
                                       input=inp,
                                       output=DummyOutput(),
                                       default='default'
                                       )).skip_if(q2=lambda x: not x['q1'])

        result = f.unsafe_ask()

        assert result == {'q1': False, 'q2': 'default'}
    finally:
        inp.close()


def test_form_checkbox_skip_using_function():
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


@pytest.mark.parametrize('comp,in1,out2', [('eq', False, ('bar',)),
                                           ('ne', True, ('bar',)),
                                           ])
def test_form_checkbox_skip_using_equality_comparison(comp, in1, out2):
    inp = create_pipe_input()
    if in1:
        text = "Y"
    else:
        text = "N"
    text += KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        q1 = questionary.confirm("Hello?",
                                 input=inp,
                                 output=DummyOutput())
        q2 = questionary.checkbox("World?",
                                  choices=[
                                      "foo",
                                      Choice("bar", checked=True)
                                  ],
                                  input=inp,
                                  output=DummyOutput(),
                                  )
        f = form(q1=q1, q2=q2).skip_if(
            q2=getattr(q1, '__{}__'.format(comp))(False))

        result = f.unsafe_ask()

        assert result['q1'] == in1 and tuple(result['q2']) == out2
    finally:
        inp.close()


numeric_tests = [
    (2, 'gt', 3, False),
    (3, 'gt', 2, True),
    (3, 'lt', 2, False),
    (2, 'lt', 3, True),
    (2, 'ge', 3, False),
    (3, 'ge', 2, True),
    (3, 'le', 2, False),
    (2, 'le', 3, True),
    (True, 'and', True, True),
    (True, 'and', False, False),
    (True, 'or', False, True),
    (False, 'or', False, False),
    (True, 'xor', False, True),
    (True, 'xor', True, False),
]


@pytest.mark.parametrize('in1,comp,comp_to,pass_test', numeric_tests)
def test_form_skip_using_numeric_comparison(in1, comp, comp_to, pass_test):
    inp = create_pipe_input()
    text = KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        q1 = questionary.select("Hello?", [Choice('a', in1), 'other'],
                                input=inp,
                                output=DummyOutput())
        q2 = questionary.select("World?", ['performed'],
                                default='skipped',
                                input=inp,
                                output=DummyOutput(),
                                )
        comparator = getattr(q1, '__{}__'.format(comp))
        if comp_to is None:
            comparison = comparator()
        else:
            comparison = comparator(comp_to)
        f = form(q1=q1, q2=q2).skip_if(q2=comparison)

        result = f.unsafe_ask()

        assert result['q1'] == in1
        if pass_test:
            assert result['q2'] == 'skipped'
        else:
            assert result['q2'] == 'performed'
    finally:
        inp.close()


@pytest.mark.parametrize('in1,comp,in2,pass_test', numeric_tests)
def test_form_skip_using_numeric_comparison_qs(in1, comp, in2, pass_test):
    inp = create_pipe_input()
    text = KeyInputs.ENTER + "\r" + KeyInputs.ENTER + "\r"

    try:
        inp.send_text(text)
        q1 = questionary.select("q1", [Choice('a', in1), 'other'],
                                input=inp,
                                output=DummyOutput())
        q2 = questionary.select("q2", [Choice('a', in2), 'other'],
                                input=inp,
                                output=DummyOutput())
        q3 = questionary.select("q3", ['performed'],
                                default='skipped',
                                input=inp,
                                output=DummyOutput(),
                                )
        comparator = getattr(q1, '__{}__'.format(comp))
        comparison = comparator(q2)
        f = form(q1=q1, q2=q2, q3=q3).skip_if(q3=comparison)

        result = f.unsafe_ask()

        assert result['q1'] == in1
        assert result['q2'] == in2
        if pass_test:
            assert result['q3'] == 'skipped'
        else:
            assert result['q3'] == 'performed'
    finally:
        inp.close()


arithmetic_tests = [
    (1, 'add', 2),
    (1, 'sub', 2),
    (1, 'mul', 2),
    (10, 'divmod', 5),
    (-1, 'abs', None),
    (9, 'truediv', 4)
]


@pytest.mark.parametrize('in1,calc,in2', arithmetic_tests)
def test_form_skip_using_arithmetic(in1, calc, in2):
    inp = create_pipe_input()
    text = KeyInputs.ENTER + "\r"
    func = getattr(in1, '__{}__'.format(calc))
    if in2 is None:
        result = func()
    else:
        result = func(in2)
    try:
        inp.send_text(text)
        q1 = questionary.select("Hello?", [Choice('a', in1), 'other'],
                                input=inp,
                                output=DummyOutput())
        q2 = questionary.select("World?", ['performed'],
                                default='skipped',
                                input=inp,
                                output=DummyOutput(),
                                )
        calculator = getattr(q1, '__{}__'.format(calc))
        if in2 is None:
            calculation = calculator()
        else:
            calculation = calculator(in2)
        f = form(q1=q1, q2=q2).skip_if(q2=calculation == result)

        result = f.unsafe_ask()

        assert result['q1'] == in1
        assert result['q2'] == 'skipped'
    finally:
        inp.close()


def test_resolve_unordered_skip_if_dependencies():
    inp = create_pipe_input()
    text = KeyInputs.ENTER + "\r"
    f = form(q2=questionary.confirm("Hello?",
                                    input=inp,
                                    output=DummyOutput()),
             q1=questionary.select("World?",
                                   choices=["foo", "bar"],
                                   input=inp,
                                   output=DummyOutput(),
                                   default='default'
                                   )).skip_if(q1=lambda x: not x['q2'])
    try:
        inp.send_text(text)
        result = f.unsafe_ask()

        assert result == {'q2': True, 'q1': 'foo'}
    finally:
        inp.close()


def test_resolve_unordered_skip_if_dependencies_fails_with_circular_deps():
    inp = create_pipe_input()
    text = KeyInputs.ENTER + "\r" + KeyInputs.ENTER + "\r"
    f = form(q2=questionary.confirm("Hello?",
                                    input=inp,
                                    output=DummyOutput()),
             q3=questionary.confirm("Hello again?",
                                    input=inp,
                                    output=DummyOutput()),
             q1=questionary.select("World?",
                                   choices=["foo", "bar"],
                                   input=inp,
                                   output=DummyOutput(),
                                   default='default'
                                   )).skip_if(q1=lambda x: not x['q2'],
                                              q2=lambda x: not x['q1'])
    try:
        with pytest.raises(DependencyError):
            inp.send_text(text)
            f.unsafe_ask()
    finally:
        inp.close()
