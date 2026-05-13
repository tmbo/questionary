from unittest import mock

from questionary import utils
from questionary.constants import DEFAULT_TERMINAL_WIDTH


def test_default_values_of():
    def f(a, b=2, c=None, *args, **kwargs):
        pass

    defaults = utils.default_values_of(f)
    assert defaults == ["b", "c", "args", "kwargs"]


def test_default_values_of_no_args():
    def f():
        pass

    defaults = utils.default_values_of(f)
    assert defaults == []


def test_arguments_of():
    def f(a, b=2, c=None, *args, **kwargs):
        pass

    defaults = utils.arguments_of(f)
    assert defaults == ["a", "b", "c", "args", "kwargs"]


def test_arguments_of_no_args():
    def f():
        pass

    defaults = utils.arguments_of(f)
    assert defaults == []


def test_filter_kwargs():
    def f(a, b=1, *, c=2):
        pass

    kwargs = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
    }

    filtered = utils.used_kwargs(kwargs, f)
    assert "a" in filtered
    assert "b" in filtered
    assert "c" in filtered
    assert "d" not in filtered


def test_filter_kwargs_empty():
    def f():
        pass

    kwargs = {
        "a": 1,
        "b": 2,
    }

    filtered = utils.used_kwargs(kwargs, f)
    assert filtered == {}


def test_required_arguments_of():
    def f(a, b=2, c=None, *args, **kwargs):
        pass

    defaults = utils.required_arguments(f)
    assert defaults == ["a"]


def test_required_arguments_of_no_args():
    def f():
        pass

    defaults = utils.required_arguments(f)
    assert defaults == []


def test_missing_arguments():
    def f(a, b=2, c=None, *args, **kwargs):
        pass

    assert utils.missing_arguments(f, {}) == {"a"}
    assert utils.missing_arguments(f, {"a": 1}) == set()
    assert utils.missing_arguments(f, {"a": 1, "b": 2}) == set()


def test_missing_arguments_of_no_args():
    def f():
        pass

    defaults = utils.missing_arguments(f, {})
    assert defaults == set()


def _fake_terminal_size(columns):
    return mock.patch(
        "questionary.utils._current_terminal_width",
        return_value=columns,
    )


def test_wrap_message_to_terminal_width_short_string_unchanged():
    with _fake_terminal_size(80):
        assert utils._wrap_message_to_terminal_width("Hello") == "Hello"


def test_wrap_message_to_terminal_width_long_string_wraps():
    long_message = (
        "Lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam "
        "nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam"
    )
    with _fake_terminal_size(40):
        wrapped = utils._wrap_message_to_terminal_width(long_message)
    assert "\n" in wrapped
    for line in wrapped.split("\n"):
        assert len(line) <= 40


def test_wrap_message_to_terminal_width_preserves_existing_newlines():
    message = "First paragraph short.\nSecond paragraph also short."
    with _fake_terminal_size(80):
        wrapped = utils._wrap_message_to_terminal_width(message)
    assert wrapped == message


def test_wrap_message_to_terminal_width_wraps_paragraph_after_newline():
    """Regression test for https://github.com/tmbo/questionary/issues/398.

    Long messages containing a trailing newline (as copier appends) must
    still be wrapped to terminal width. Before the fix, prompt-toolkit split
    on the last newline and rendered the leading paragraph in a non-wrapping
    window, so long lines overflowed the terminal.
    """
    long_first = ("word " * 50).strip()  # 249 chars of breakable text
    message = f"{long_first}\n"
    with _fake_terminal_size(80):
        wrapped = utils._wrap_message_to_terminal_width(message)
    # No line in the first paragraph should exceed terminal width.
    first_paragraph = wrapped.split("\n\n")[0] if "\n\n" in wrapped else wrapped
    for line in first_paragraph.split("\n"):
        assert len(line) <= 80


def test_wrap_message_to_terminal_width_respects_prefix_width():
    long_message = "word " * 30
    with _fake_terminal_size(40):
        wrapped = utils._wrap_message_to_terminal_width(long_message, prefix_width=10)
    # First line wraps at width - prefix_width (40 - 10 = 30).
    first_line = wrapped.split("\n")[0]
    assert len(first_line) <= 30


def test_wrap_message_to_terminal_width_passes_through_non_string():
    formatted = [("class:question", "hello")]
    assert utils._wrap_message_to_terminal_width(formatted) is formatted


def test_wrap_message_to_terminal_width_passes_through_empty_string():
    assert utils._wrap_message_to_terminal_width("") == ""


def test_wrap_message_to_terminal_width_handles_unbreakable_long_word():
    # `break_long_words=False` means a single very long word can't be split.
    # The function should still return the message without crashing.
    long_word = "a" * 200
    with _fake_terminal_size(40):
        wrapped = utils._wrap_message_to_terminal_width(long_word)
    assert long_word in wrapped


def test_current_terminal_width_falls_back_on_os_error():
    with mock.patch(
        "questionary.utils.shutil.get_terminal_size",
        side_effect=OSError("no tty"),
    ), mock.patch(
        "questionary.utils.get_app_or_none",
        return_value=None,
    ):
        assert utils._current_terminal_width() == DEFAULT_TERMINAL_WIDTH


def test_wrap_message_to_terminal_width_falls_back_on_os_error():
    with mock.patch(
        "questionary.utils.shutil.get_terminal_size",
        side_effect=OSError("no tty"),
    ), mock.patch(
        "questionary.utils.get_app_or_none",
        return_value=None,
    ):
        # Falls back to DEFAULT_TERMINAL_WIDTH; a 200-char message should
        # still wrap.
        wrapped = utils._wrap_message_to_terminal_width("x " * 100)
    assert "\n" in wrapped


def test_current_terminal_width_prefers_active_app():
    fake_app = mock.Mock()
    fake_app.output.get_size.return_value = mock.Mock(columns=42, rows=24)
    with mock.patch(
        "questionary.utils.get_app_or_none",
        return_value=fake_app,
    ):
        # Even with shutil reporting something else, the app's size wins.
        with mock.patch(
            "questionary.utils.shutil.get_terminal_size",
            return_value=mock.Mock(columns=999, lines=24),
        ):
            assert utils._current_terminal_width() == 42


def test_current_terminal_width_falls_through_when_app_reports_zero():
    # An active app reporting 0 columns (degenerate) should not be trusted;
    # the function falls through to shutil.
    fake_app = mock.Mock()
    fake_app.output.get_size.return_value = mock.Mock(columns=0, rows=24)
    with mock.patch(
        "questionary.utils.get_app_or_none",
        return_value=fake_app,
    ), mock.patch(
        "questionary.utils.shutil.get_terminal_size",
        return_value=mock.Mock(columns=120, lines=24),
    ):
        assert utils._current_terminal_width() == 120


def test_current_terminal_width_falls_back_when_shutil_reports_zero():
    with mock.patch(
        "questionary.utils.get_app_or_none",
        return_value=None,
    ), mock.patch(
        "questionary.utils.shutil.get_terminal_size",
        return_value=mock.Mock(columns=0, lines=24),
    ):
        assert utils._current_terminal_width() == DEFAULT_TERMINAL_WIDTH


def test_wrap_message_to_terminal_width_pathologically_narrow_returns_unchanged():
    with _fake_terminal_size(1):
        assert utils._wrap_message_to_terminal_width("hello world") == "hello world"
