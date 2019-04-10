# -*- coding: utf-8 -*-
import inspect

ACTIVATED_ASYNC_MODE = False


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


async def activate_prompt_toolkit_async_mode():
    """Configure prompt toolkit to use the asyncio event loop.

    Needs to be async, so we use the right event loop in py 3.5"""
    from prompt_toolkit.eventloop import use_asyncio_event_loop

    global ACTIVATED_ASYNC_MODE

    # Tell prompt_toolkit to use asyncio for the event loop.
    use_asyncio_event_loop()
    ACTIVATED_ASYNC_MODE = True
