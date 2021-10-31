"""Module for prompting for dates.


This module provides a prompting method for dates and times. Two basic types of
completion and validation are provided: :class: `SimpleDateCompleter` and :class:
`ParsingDateCompleter`. The former one, using only the build in module :module:
`datetime`, whereas the latter one offers the option to use third part libraries, e.g.
as `dateutil`_ or `dateparser`_, for completion. Similar class are there for validation
(:class: `SimpleDateValidator` and :class: `ParsingDateValidator`) Note that the
'simple' completer and validator currently only supports dates and not times, but the
'parsing' ones may support times as well (depending on the used third part library).
Both ``Completer`` and ``Validator``, the 'simple' and the 'parsing' ones are combined
in :class: `FullDateCompleter` and :class: `FullDateValidator`.

Typical usage could look like this:

Example:
    >>> import questionary
    >>> import dateutil
    >>> questionary.date("Type a date: ").ask()
    ? Type a date: 2021-01-01
    '2021-01-01'
    >>> questionary.date("Type a date or time: ", parser=dateutil.parser.parse).ask()
    ? Type a date or time: 2021-01-01 00:00:00
    '2021-01-01 00:00:00'

.. _dateparser: https://github.com/scrapinghub/dateparser
.. _dateutil: https://github.com/dateutil/dateutil
"""

from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import datetime

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text.base import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_processor import KeyPressEvent
from prompt_toolkit.keys import Keys
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.shortcuts.prompt import CompleteStyle
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.styles import merge_styles
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.validation import Validator

from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.constants import DEFAULT_STYLE
from questionary.prompts.common import build_validator
from questionary.question import Question

# date format according to ISO8601
ISO8601 = "%Y-%m-%d"

# list of supported date formats
SUPPORTED_FORMATS = [
    ISO8601,
    "%d.%m.%Y",
    "%d-%m-%Y",
    # ISO8601,
    # "%d.%m.%y",
    # "%d-%m-%y",
    "%m-%d-%Y",
    "%m/%d/%Y",
    "%m.%d.%Y",
]

# lists of completions (currently only numbers)
DAY = [str(i) for i in range(1, 32)]
MONTH = [str(i) for i in range(1, 13)]
YEAR = ["0" * (4 - len(str(i))) + str(i) for i in range(9999)]
HOUR = [str(i) for i in range(0, 24)]
MINUTE = [str(i) for i in range(60)]

# dict used to determine correct order for completions
PARSE_FORMAT_DICT = {"%d": DAY, "%m": MONTH, "%Y": YEAR, "%H": HOUR, "%M": MINUTE}


AnyDate = Union[datetime.date, datetime.datetime, None]


###################################
#  SIMPLE COMLETION AND VALIDATION
###################################


class SimpleDateCompleter(Completer):
    def __init__(self, date_format: Optional[str] = None) -> None:
        """__init__ of :class: `DateCompleter`.

        Offers completions for a date according to the chosen format.

        Args:
            date_format (str): Format determining the format that is to be used
                for parsing :class: `datetime.date`.

        Raises:
            ValueError: if ``date_format`` is not in ``SUPPORTED_FORMATS``.
        """
        self.format: str = date_format or ISO8601
        if self.format not in SUPPORTED_FORMATS:
            raise (
                ValueError(
                    f"Date format '{self.format}' is not supported.\nSupported"
                    f" formats:\n{SUPPORTED_FORMATS}"
                )
            )
        self.delimeter: str = self.format[-3]

    def _get_parse_order(self) -> List[str]:
        """Returns the order for completions.

        Parses ``self.date_format`` into a list representing the order for completions,
        e.g. [YEAR, MONTH, DAY].
        """
        parse_order = self.format.split(self.delimeter)
        return [PARSE_FORMAT_DICT.get(item) for item in parse_order]

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Completion of text input following a given ``date_format``.

        According what has allready been typed and the given ``date_format``
        completions for year, month and day are given (numbers only).
        Date format ``date_format`` needs to be one of the ``SUPPORTED_FORMATS´´.
        Supports only dates at the moment.

        Args:
            document (Document): The :class: `prompt_toolkit.document.Document` created
                from the user input.
            complete_event (CompleteEvent): The complete event.

        Yields:
            Iterator[Iterable[Completion]]: The completions
        """
        text_split = document.text.split(self.delimeter)
        # the date information the user is currently typing, i.e. year, month or day
        user_input = text_split[-1]
        # old_input is the text the user has already typed
        old_input = (
            self.delimeter.join(text_split[:-1]) + self.delimeter
            if len(text_split) > 1
            else ""
        )
        # get correct list of completion options
        completion_list = self._get_parse_order()[len(text_split) - 1]
        # find fitting completions in completion_list
        for entry in completion_list:
            if entry.startswith(user_input):
                completion = entry if int(entry) >= 10 else "0" + entry
                completion += self.delimeter if len(text_split) < 3 else ""
                yield Completion(
                    old_input + completion,
                    start_position=-len(document.text),
                    style="fg:ansigreen bold",
                    selected_style="fg:white bg:ansired bold",
                    display=completion,
                )


class SimpleDateValidator(Validator):
    def __init__(self, date_format: Optional[str] = None) -> None:
        """__init__ of :class: `DateValidator`.

        Validates given input for dates.

        Args:
            date_format (str): Format determining the format that is to be used
                for parsing :class: `datetime.date`.
        """
        self.format: str = date_format or ISO8601
        if self.format not in SUPPORTED_FORMATS:
            raise (
                ValueError(
                    f"Date format '{self.format}' is not supported.\nSupported"
                    f" formats:\n{SUPPORTED_FORMATS}"
                )
            )

    def validate(self, document: Document) -> None:
        """Validates the user input.

        Only inputs that can be parsed into `dateobject`_ via the `datetime-parser`_ are
        accepted.

        Args:
            document (Document): The :class: `prompt_toolkit.document.Document` created
                from the user input.

        Raises:
            ValidationError: if parsing text input via ``datetime.datetime.strptime``
                fails.

        .. _dateobject: :class: `datetime.datetime`
        .. _datetime_parser: :function: `datetime.datetime.strptime`
        """
        try:
            datetime.datetime.strptime(document.text, self.format)
        except Exception:
            raise (ValidationError(message="Invalid date."))


###################################
#  PARSING COMLETION AND VALIDATION
###################################


class ParsingDateCompleter(Completer):
    def __init__(self, parser: Optional[Callable[[str], AnyDate]] = None) -> None:
        """__init__ of :class: `ParsingDateCompleter`.

        Completes the date using a parser.

        Args:
            parser (Optional[Callable[str], AnyDate], optional): A callable that parses
                a string into a :class: `datetime.date` or :class: `datetime.date`, e.g.
                the ones from `dateparser`_ or `dateutil`_. Defaults to None.

        .. _dateparser: https://github.com/scrapinghub/dateparser
        .. _dateutil: https://github.com/dateutil/dateutil
        """
        self.parser = parser or (lambda: None)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Completions using a date parser.

        Calls a parser, which converts the string typed by the user into some date
        object (:class: `datetime.date` or :class: `datetime.date`) and yields its
        string as the completion.

        Args:
            document (Document): The :class: `prompt_toolkit.document.Document` created
                from the user input.
            complete_event (CompleteEvent): The complete event.

        Yields:
            Iterator[Iterable[Completion]]: The completions
        """
        try:
            parsed_date = self.parser(document.text)
        except Exception:
            parsed_date = None
        # if input can be parsed, yield the string of the parsed date as completion
        if parsed_date is not None:
            yield Completion(str(parsed_date), start_position=-len(document.text))
