# -*- coding: utf-8 -*-
import inspect


def default_values_of(func):
    """Return the defaults of the function `func`."""

    signature = inspect.signature(func)
    return [k
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty or
            v.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD]


def arguments_of(func):
    """Return the parameters of the function `func`."""

    return list(inspect.signature(func).parameters.keys())


def required_arguments(func):
    """Return all arguments of a function that do not have a default value."""
    defaults = default_values_of(func)
    args = arguments_of(func)

    if defaults:
        args = args[:-len(defaults)]
    return args  # all args without default values


def missing_arguments(func, argdict):
    """Return all arguments that are missing to call func."""
    return set(required_arguments(func)) - set(argdict.keys())
