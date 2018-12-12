from tests.utils import KeyInputs, patched_prompt


def test_confirm_example():
    from examples.dict_style.confirm import questions
    text = "n" + KeyInputs.ENTER + "\r"

    result = patched_prompt(questions, text)
    assert result == {'continue': False, 'exit': False}


def test_input_example():
    from examples.dict_style.text import questions
    text = (KeyInputs.ENTER + KeyInputs.ENTER + "1234567890" +
            KeyInputs.ENTER + "\r")

    result = patched_prompt(questions, text)
    assert result == {'first_name': '',
                      'last_name': 'Doe',
                      'phone': '1234567890'}


def test_list_example():
    from examples.dict_style.select import questions
    text = "n" + KeyInputs.ENTER + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result = patched_prompt(questions, text)
    assert result == {'delivery': 'bike',
                      'size': 'jumbo',
                      'theme': 'Order a pizza'}


def test_rawlist_example():
    from examples.dict_style.rawselect import questions
    text = "3" + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result = patched_prompt(questions, text)
    assert result == {'theme': 'Ask opening hours', 'size': 'jumbo'}


def test_checkbox_example_dict():
    from examples.dict_style.checkbox import questions
    text = "n" + KeyInputs.ENTER + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result = patched_prompt(questions, text)
    assert result == {'toppings': ['foo']}


def test_checkbox_example_dict():
    from examples.checkbox import question
    text = "n" + KeyInputs.ENTER + KeyInputs.ENTER + KeyInputs.ENTER + "\r"

    result = patched_prompt(question, text)
    assert result == {'toppings': ['foo']}


def test_password_example():
    from examples.dict_style.password import questions
    text = "asdf" + KeyInputs.ENTER + "\r"

    result = patched_prompt(questions, text)
    assert result == {'password': 'asdf'}
