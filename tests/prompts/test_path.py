# -*- coding: utf-8 -*-
import prompt_toolkit
import pytest

from tests.utils import KeyInputs, feed_cli_with_input
from prompt_toolkit.completion import Completer, Completion


@pytest.fixture
def path_completion_tree(tmp_path):
    needed_directories = [
        tmp_path / "foo",
        tmp_path / "foo" / "buz",  # alphabetically after baz.any
        tmp_path / "bar",
        tmp_path / "baz",
    ]

    needed_files = [tmp_path / "foo" / "baz.any", tmp_path / "foo" / "foobar.any"]

    for d in needed_directories:
        d.mkdir()

    for f in needed_files:
        f.open("a").close()
    return tmp_path


def test_path():
    message = "Pick your path "
    text = "myfile.py" + KeyInputs.ENTER
    result, cli = feed_cli_with_input("path", message, text)
    assert result == "myfile.py"


@pytest.mark.skipif(
    prompt_toolkit.__version__.startswith("2"), reason="requires prompt toolkit >= 3.0"
)
def test_complete_path(path_completion_tree):
    test_input = str(path_completion_tree / "ba")
    message = "Pick your path"
    texts = [
        test_input,
        KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER,
        KeyInputs.ENTER,
    ]

    result, cli = feed_cli_with_input("path", message, texts)
    assert result == str(path_completion_tree / "baz")


@pytest.mark.skipif(
    prompt_toolkit.__version__.startswith("2"), reason="requires prompt toolkit >= 3.0"
)
def test_complete_requires_explicit_enter(path_completion_tree):
    # checks that an autocomplete needs to be confirmed with an enter and that the
    # enter doesn't directly submit the result
    test_input = str(path_completion_tree / "ba")
    message = "Pick your path"
    texts = [
        test_input,
        KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER,
        "foo" + KeyInputs.ENTER,
    ]

    result, cli = feed_cli_with_input("path", message, texts)

    assert result == str(path_completion_tree / "baz" / "foo")


@pytest.mark.skipif(
    prompt_toolkit.__version__.startswith("2"), reason="requires prompt toolkit >= 3.0"
)
def test_complete_path_directories_only(path_completion_tree):
    test_input = str(path_completion_tree / "foo" / "b")
    message = "Pick your path"
    texts = [test_input, KeyInputs.TAB + KeyInputs.ENTER, KeyInputs.ENTER]

    result, cli = feed_cli_with_input("path", message, texts, only_directories=True)
    assert result == str(path_completion_tree / "foo" / "buz")


@pytest.mark.skipif(
    prompt_toolkit.__version__.startswith("2"), reason="requires prompt toolkit >= 3.0"
)
def test_complete_custom_completer():
    test_path = "foobar"

    class CustomCompleter(Completer):
        def get_completions(self, _, __):
            yield Completion(test_path)

    message = "Pick your path"
    texts = ["baz", KeyInputs.TAB + KeyInputs.ENTER, KeyInputs.ENTER]

    result, cli = feed_cli_with_input(
        "path", message, texts, completer=CustomCompleter()
    )
    assert result == "baz" + test_path
