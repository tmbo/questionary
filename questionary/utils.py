# -*- coding: utf-8 -*-
from __future__ import print_function

import inspect


def default_values_of(func):
    """Return the defaults of the function `func`."""

    try:
        # python 3.x is used
        signature = inspect.signature(func)
        return [k
                for k, v in signature.parameters.items()
                if v.default is not inspect.Parameter.empty or
                v.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD]
    except AttributeError:
        # python 2.x is used
        # noinspection PyDeprecation
        return list(inspect.getargspec(func).defaults)


def arguments_of(func):
    """Return the parameters of the function `func`."""

    try:
        # python 3.x is used
        return list(inspect.signature(func).parameters.keys())
    except AttributeError:
        # python 2.x is used
        # noinspection PyDeprecation
        return list(inspect.getargspec(func).args)


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
