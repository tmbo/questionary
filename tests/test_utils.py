from questionary import utils


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
