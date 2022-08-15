from prompt_toolkit.output import DummyOutput

from tests.utils import KeyInputs
from tests.utils import execute_with_input_pipe


def ask_with_patched_input(q, text):
    def run(inp):
        inp.send_text(text)
        return q(input=inp, output=DummyOutput())

    return execute_with_input_pipe(run)


def test_confirm_example():
    from examples.confirm_continue import ask_dictstyle
    from examples.confirm_continue import ask_pystyle

    text = "n" + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"continue": False}
    assert result_dict["continue"] == result_py


def test_text_example():
    from examples.text_phone_number import ask_dictstyle
    from examples.text_phone_number import ask_pystyle

    text = "1234567890" + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"phone": "1234567890"}
    assert result_dict["phone"] == result_py


def test_select_example():
    from examples.select_restaurant import ask_dictstyle
    from examples.select_restaurant import ask_pystyle

    text = KeyInputs.DOWN + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"theme": "Make a reservation"}
    assert result_dict["theme"] == result_py


def test_rawselect_example():
    from examples.rawselect_separator import ask_dictstyle
    from examples.rawselect_separator import ask_pystyle

    text = "3" + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"theme": "Ask opening hours"}
    assert result_dict["theme"] == result_py


def test_checkbox_example():
    from examples.checkbox_separators import ask_dictstyle
    from examples.checkbox_separators import ask_pystyle

    text = "n" + KeyInputs.ENTER + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"toppings": ["foo"]}
    assert result_dict["toppings"] == result_py


def test_password_example():
    from examples.password_git import ask_dictstyle
    from examples.password_git import ask_pystyle

    text = "asdf" + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"password": "asdf"}
    assert result_dict["password"] == result_py


def test_autocomplete_example():
    from examples.autocomplete_ants import ask_dictstyle
    from examples.autocomplete_ants import ask_pystyle

    text = "Polyergus lucidus" + KeyInputs.ENTER + "\r"

    result_dict = ask_with_patched_input(ask_dictstyle, text)
    result_py = ask_with_patched_input(ask_pystyle, text)

    assert result_dict == {"ants": "Polyergus lucidus"}
    assert result_py == "Polyergus lucidus"


def test_advanced_workflow_example():
    from examples.advanced_workflow import ask_dictstyle

    text = (
        KeyInputs.ENTER
        + "questionary"
        + KeyInputs.ENTER
        + KeyInputs.DOWN
        + KeyInputs.DOWN
        + KeyInputs.ENTER
        + "Hello World"
        + KeyInputs.ENTER
        + "\r"
    )

    result_dict = ask_with_patched_input(ask_dictstyle, text)

    assert result_dict == {
        "intro": None,
        "conditional_step": True,
        "next_question": "questionary",
        "second_question": "Hello World",
    }
