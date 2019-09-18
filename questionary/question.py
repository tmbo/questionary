import sys

import prompt_toolkit.patch_stdout

from questionary import utils
from questionary.constants import DEFAULT_KBI_MESSAGE
from typing import Any, Union

__all__ = ['Question']


class FrozenOperationMixin:
    def __eq__(self, other: object):
        return FrozenOperation('eq', self, other)

    def __ne__(self, other: object):
        return FrozenOperation('ne', self, other)

    def __gt__(self, other: object):
        return FrozenOperation('gt', self, other)

    def __lt__(self, other: object):
        return FrozenOperation('lt', self, other)

    def __and__(self, other: object):
        return FrozenOperation('and', self, other)

    def __or__(self, other: object):
        return FrozenOperation('or', self, other)

    def __le__(self, other: object):
        return FrozenOperation('le', self, other)

    def __ge__(self, other: object):
        return FrozenOperation('ge', self, other)

    def __xor__(self, other: object):
        return FrozenOperation('xor', self, other)

    def __add__(self, other: object):
        return FrozenOperation('add', self, other)

    def __sub__(self, other: object):
        return FrozenOperation('sub', self, other)

    def __mul__(self, other: object):
        return FrozenOperation('mul', self, other)

    def __divmod__(self, other: object):
        return FrozenOperation('divmod', self, other)

    def __abs__(self):
        return FrozenOperation('abs', self)

    def __truediv__(self, other: object):
        return FrozenOperation('truediv', self, other)


class Question(FrozenOperationMixin):
    """A question to be prompted.

    This is an internal class. Questions should be created using the
    predefined questions (e.g. text or password)."""

    def __init__(self, application: prompt_toolkit.Application, default=None):
        self.application = application
        self.should_skip_question = False
        self.default = default

    def __hash__(self):
        return hash(str(hash(self.application)) + str(self.default) + str(self.should_skip_question))

    async def ask_async(self,
                        patch_stdout: bool = False,
                        kbi_msg: str = DEFAULT_KBI_MESSAGE) -> Any:
        """Ask the question using asyncio and return user response."""

        if self.should_skip_question:
            return self.default

        try:
            sys.stdout.flush()
            return await self.unsafe_ask_async(patch_stdout)
        except KeyboardInterrupt:
            print("\n{}\n".format(kbi_msg))
            return None

    def ask(self,
            patch_stdout: bool = False,
            kbi_msg: str = DEFAULT_KBI_MESSAGE) -> Any:
        """Ask the question synchronously and return user response."""

        if self.should_skip_question:
            return self.default

        try:
            return self.unsafe_ask(patch_stdout)
        except KeyboardInterrupt:
            print("\n{}\n".format(kbi_msg))
            return None

    def unsafe_ask(self, patch_stdout: bool = False) -> Any:
        """Ask the question synchronously and return user response.

        Does not catch keyboard interrupts."""

        if patch_stdout:
            with prompt_toolkit.patch_stdout.patch_stdout():
                return self.application.run()
        else:
            return self.application.run()

    def skip_if(self, condition: bool, default: Any = None) -> 'Question':
        """Skip the question if flag is set and return the default instead."""

        self.should_skip_question = condition
        self.default = default
        return self

    async def unsafe_ask_async(self, patch_stdout: bool = False) -> Any:
        """Ask the question using asyncio and return user response.

        Does not catch keyboard interrupts."""

        if not utils.ACTIVATED_ASYNC_MODE:
            await utils.activate_prompt_toolkit_async_mode()

        if patch_stdout:
            # with prompt_toolkit.patch_stdout.patch_stdout():
            return await self.application.run_async().to_asyncio_future()
        else:
            return await self.application.run_async().to_asyncio_future()


class FrozenOperation(FrozenOperationMixin):
    def __init__(self, action: Union[str, None], a: Any, b: Any = None):
        self.action = action
        self.a = a
        self.b = b

    def __call__(self, values: dict) -> object:
        if isinstance(self.a, FrozenOperation):
            a = self.a(values)
        elif isinstance(self.a, Question):
            a = values[self.a]
        else:
            a = self.a

        if self.action is None:
            return a

        if isinstance(self.b, FrozenOperation):
            b = self.b(values)
        elif isinstance(self.b, Question):
            b = values[self.b]
        else:
            b = self.b

        if b is None:
            return getattr(a, '__' + self.action + '__')()
        return getattr(a, '__' + self.action + '__')(b)
