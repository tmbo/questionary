"""Module for prompting for dates.


Core of this module forms the function :function: `date`, which allows to prompt for for
dates and times with completion and validation. Two basic types of completion and
validation are provided: :class: `SimpleDateCompleter` and :class:
`ParsingDateCompleter`. The former one, using only the build in module :module:
`datetime`, whereas the latter one offers the option to easily include third part
libraries, e.g. as `dateutil`_ or `dateparser`_, for completion. Similar class are there
for validation (:class: `SimpleDateValidator` and :class: `ParsingDateValidator`). Note
that the 'simple' completer and validator currently only supports dates or times, but
not both at the same time. The 'parsing' ones, on the other hand, may support times as
well (depending on the used third part library). Both ``Completer`` and ``Validator``,
the 'simple' and the 'parsing' ones are combined in :class: `FullDateCompleter` and
:class: `FullDateValidator`. If no parser is given to the 'full' completer and
validator, :function: `custom_date_parser` is used by default. If you want to deactivate
'parsing' validation and completion, you need to call :function: `date` with
``no_extra_parser`` set to True.

By default date returns an :class: `datetime.datetime` instance.

Typical usage could look like this:

Example:
    >>> import questionary
    >>> import dateutil.parser
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

import re
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
ISO8601_TIME = "%H:%M:%S"

# list of supported date formats
SUPPORTED_FORMATS = [
    ISO8601,
    ISO8601_TIME,
    "%d.%m.%Y",
    "%d-%m-%Y",
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
SECOND = [str(i) for i in range(60)]

# dict used to determine correct order for completions
PARSE_FORMAT_DICT = {
    "%d": DAY,
    "%m": MONTH,
    "%Y": YEAR,
    "%H": HOUR,
    "%M": MINUTE,
    "%S": SECOND,
}


AnyDate = Union[datetime.date, datetime.datetime, None]


def custom_date_parser(input: str) -> Optional[datetime.date]:
    """A very simple date parser.

    Tries to parse text inputs into :class: ´datetime.datetime` objects. Assumes
    the input to follow ISO8601_.

    Args:
        input (str): Text input that is to be parsed.

    Returns:
        Optional[datetime.date]: The parsed :class: `datetime.datetime` instance. None,
            if parsing fails.

    Example:
        >>> from questionary import date
        >>> _date = date.custom_date_parser("2021-01-01 00:00:00")
        >>> print(f"The formatted date is: {_date}.")
        The formatted date is: 2021-01-01 00:00:00.
        >>> assert _date == datetime.datetime(2021, 1, 1, 0, 0)
        >>> _date_weird = date.custom_date_parser("2021.01 some 01 at time 12  :30")
        >>> assert _date_weird == datetime.datetime(2021, 1, 1, 0, 0)
        >>> print(f"The formatted date is: {_date_weird}.")
        The formatted date is: 2021-01-01 00:00:00.
        >>> assert date.custom_date_parser("this is no date') is None

    .. _ISO8601: https://en.wikipedia.org/wiki/ISO_8601
    """
    _time_format_codes = ["%Y", "%m", "%d", "%H", "%M", "%S", "%f"]
    date_formats = [
        "".join(_time_format_codes[0:i]) for i in range(1, len(_time_format_codes) + 1)
    ]

    def _try_date_format(date_format: str, text: str) -> Optional[datetime.datetime]:
        """Tries to parse ``text`to :class: `datetime.datetime`."""
        try:
            return datetime.datetime.strptime(text, date_format)
        except Exception:
            return None

    # remove all delimeters from the input
    pattern = re.compile(r"[\d]")
    relevant_input = "".join(pattern.findall(input))
    # try parsing for the several date_formats
    for date_format in date_formats:
        _date = _try_date_format(date_format=date_format, text=relevant_input)
        # if parsing succeeded return the result
        if _date is not None:
            return _date
    # no parsing succeeded so return None
    return None


###################################
#  SIMPLE COMPLETION AND VALIDATION
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

    def _get_parse_order(self) -> List[List[str]]:
        """Returns the order for completions.

        Parses ``self.date_format`` into a list representing the order for completions,
        e.g. [YEAR, MONTH, DAY].
        """
        parse_order = self.format.split(self.delimeter)
        return [PARSE_FORMAT_DICT.get(item) for item in parse_order]  # type: ignore[misc]

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Completion of text input following a given ``date_format``.

        According what has already been typed and the given ``date_format``
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

        Raises:
            ValueError: if ``parser`` is neither None nor a callable.

        .. _dateparser: https://github.com/scrapinghub/dateparser
        .. _dateutil: https://github.com/dateutil/dateutil
        """
        self.parser = parser or custom_date_parser
        if not callable(self.parser):
            raise (
                ValueError(
                    f"'parser' needs to be a callable (not a {type(parser).__name__})."
                )
            )

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


class ParsingDateValidator(Validator):
    """Validator class for date validation via a parser."""

    def __init__(self, parser: Optional[Callable[[str], AnyDate]] = None) -> None:
        """__init__ of :class: `ParsingDateValidator`.

        Validates the string input for :function: `date` using a parser.

        Args:
            parser (Optional[Callable[str], AnyDate], optional): A callable that parses
                a string into a :class: `datetime.date` or :class: `datetime.date`, e.g.
                the ones from `dateparser`_ or `dateutil`_. Defaults to None.

        Raises:
            ValueError: if ``parser`` is neither None nor a callable

        .. _dateparser: https://github.com/scrapinghub/dateparser
        .. _dateutil: https://github.com/dateutil/dateutil
        """
        self.parser = parser or custom_date_parser
        if not callable(self.parser):
            raise (
                ValueError(
                    f"'parser' needs to be a callable (not a {type(parser).__name__})."
                )
            )

    def validate(self, document: Document) -> None:
        """Validates the date input using a date parser.

        If `self.parser` is None, no validation is performed. Otherwise, only those
        inputs that can be parsed to a valid dateobject (:class: `datetime.date` or
        :class: `datetime.date`) are considered to be valid.

        Args:
            document (Document): The :class: `prompt_toolkit.document.Document` created
                of the user input.

        Raises:
            ValidationError: if parsing text input via ``self.parser`` fails.
        """
        try:
            parsed_date = self.parser(document.text)
        except Exception:
            parsed_date = None
        if self.parser is not None:
            if parsed_date is None:
                raise (ValidationError(message="Can not parse input to date object."))


###################################
#  FULL COMLETION AND VALIDATION
###################################


class FullDateCompleter(Completer):
    """Completer for date prompts.

    Yields completions from both :class: `SimpleDateCompleter´ and :class:
    `ParsingDateCompleter`
    """

    def __init__(
        self,
        date_format: Optional[str] = ISO8601,
        parser: Optional[Callable[[str], AnyDate]] = None,
    ) -> None:
        """Completer for date prompts.

        Yields completions from both :class: `SimpleDateCompleter´ and :class:
        `ParsingDateCompleter`

        Args:
            date_format (str): Format determining the format that is to be used
                for parsing :class: `datetime.date`. If set to None, completion of
                :class: `SimpleDateCompleter´ is deactivated. Defaults to ´´ISO8601``.
            parser (Optional[Callable[str], AnyDate], optional): A callable that parses
                a string into a :class: `datetime.date` or :class: `datetime.date`, e.g.
                the ones from `dateparser`_ or `dateutil`_. Defaults to None.

        .. _dateparser: https://github.com/scrapinghub/dateparser
        .. _dateutil: https://github.com/dateutil/dateutil
        """
        self.date_format = date_format
        self.parser = parser
        self.simple_completer = SimpleDateCompleter(date_format=date_format)
        self.parsing_completer = ParsingDateCompleter(parser=parser)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Completion method of :class: `FullDateCompleter`.

        Yields completions from both :class: `SimpleDateCompleter´ and :class:
        `ParsingDateCompleter`


        Args:
            document (Document): The :class: `prompt_toolkit.document.Document` created
                from the user input.
            complete_event (CompleteEvent): The complete event.

        Yields:
            Iterator[Iterable[Completion]]: The completions
        """
        if self.date_format is not None:
            simple_completions = (
                self.simple_completer.get_completions(document, complete_event) or []
            )
        else:
            simple_completions = []
        parsed_completions = (
            self.parsing_completer.get_completions(document, complete_event) or []
        )
        if self.parser is None:
            parsed_completions = []
        for completion in simple_completions:
            yield completion
        for completion in parsed_completions:
            yield completion


class FullDateValidator(Validator):
    """Validation of user input for :function: `date`.

    Validates the user input for :func: `date` via calling validation of :class:
    `ParsingDateValidator` (if ``parsing`` is a callable) or via calling ``validate`` of
    :class: `SimpleDateValidator`.

        Args:
            date_format (str): Format determining the format that is to be used
                for parsing :class: `datetime.date`.
            parser (Callable[[str], AnyDate], optional): A callable that parses
                a string into a :class: `datetime.date` or :class: `datetime.date`, e.g.
                the ones from `dateparser`_ or `dateutil`_. Defaults to None.

        .. _dateparser: https://github.com/scrapinghub/dateparser
        .. _dateutil: https://github.com/dateutil/dateutil
    """

    def __init__(
        self,
        date_format: Optional[str] = ISO8601,
        parser: Optional[Callable[[str], AnyDate]] = None,
    ) -> None:
        """__init__ of :class: `FullDateValidator`.

        Validates the user input for :func: `date` via calling validation of :class:
        `ParsingDateValidator` (if ``parser`` is a callable) or via calling
        ``validate`` of :class: `SimpleDateValidator`.

        Args:
            date_format (str): Format determining the format that is to be used
                for parsing :class: `datetime.date`. Defaults to ``ISO8601``.
            parser (Callable[[str], AnyDate], optional): A callable that parses
                a string into a :class: `datetime.date` or :class: `datetime.date`, e.g.
                the ones from `dateparser`_ or `dateutil`_. Defaults to None.

        .. _dateparser: https://github.com/scrapinghub/dateparser
        .. _dateutil: https://github.com/dateutil/dateutil
        """
        self.date_format = date_format
        self.parser = parser
        self.simple_validator = SimpleDateValidator(date_format=date_format)
        self.parsing_validator = ParsingDateValidator(parser=parser)

    def validate(self, document: Document) -> None:
        """Validaton of user input for :function: `date`.

        Validates the user input for :func: `date` via calling validation of :class:
        `ParsingDateValidator` (if ``parsing`` is a callable) or via calling
        ``validate`` of :class: `SimpleDateValidator`.

        Args:
            document (Document): The :class: `prompt_toolkit.document.Document` created
                of the user input.
        """
        if self.parser is None:
            self.simple_validator.validate(document)
        else:
            self.parsing_validator.validate(document)


###################################
#            THE PROMPT
###################################


def date(
    message: str,
    default: str = "",
    qmark: str = DEFAULT_QUESTION_PREFIX,
    validate: Any = None,
    completer: Completer = None,
    style: Optional[Style] = None,
    date_format: Optional[str] = ISO8601,
    print_date_format: bool = True,
    parser: Optional[Callable[[str], AnyDate]] = None,
    no_extra_parser: bool = False,
    return_date_object: bool = True,
    complete_style: CompleteStyle = CompleteStyle.MULTI_COLUMN,
    **kwargs: Any,
) -> Question:
    """A text input for a date or time with autocompletion enabled.

    Args:
        message (str): Question text.
        default (str): Default return value (single value). Defaults to "".
        qmark (str): Question prefix displayed in front of the question. By default this
            is a ``?``. Defaults to DEFAULT_QUESTION_PREFIX.
        validate (Any, optional): Require the entered value to pass a validation. The
            value can not be submitted until the validator accepts it (e.g. to check
        minimum password length). This can either be a function accepting the input and
        returning a boolean, or an class reference to a subclass of the prompt toolkit
        Validator class. Defaults to None.
        completer (Completer, optional): A :class: `prompt_toolkit.completion.Completer`
            yielding completions for user input. If None, :class: `FullDateCompleter` is
            used. Defaults to None. Defaults to None.
        style (Style, optional): A custom color and style for the question parts. You
            can configure colors as well as font types for different elements.
            Defaults to None.
        date_format (str, optional): Format determining the format that is to be used
            for parsing :class: `datetime.date`. If set to None (and no ``completer`` was
            set) completions of :class: `SimpleDateCompleter` are deactivated.Defaults to
            ``ISO8601``.. Defaults to ISO8601.
        print_date_format (bool): If set to True, ``date_format`` is printed on the
            right of the prompt. Defaults to True.
        parser (Callable[[str], AnyDate], optional): A callable that parses
                a string into a :class: `datetime.date` or :class: `datetime.date`, e.g.
                the ones from `dateparser`_ or `dateutil`_. If None, set to
                :function: `custom_date_parser`. Defaults to None.
                Has no effect is ``no_extra_parser`` is set to True.
        no_extra_parser (bool): If True, completion and validation using the ``parser`` is
            not performed. Defaults to False.
        return_date_object (bool): If True, a parsed date object is returned. Else, string
            the text input is returned. Defaults to True.
        complete_style (CompleteStyle): How autocomplete menu would be shown, it could
            be ``COLUMN`` ``MULTI_COLUMN`` or ``READLINE_LIKE`` from
            :class:`prompt_toolkit.shortcuts.CompleteStyle`. Defaults to
            CompleteStyle.MULTI_COLUMN.

    Returns:
        :class:`Question`: Question instance, ready to be prompted (using ``.ask()``).

    Example:
        >>> import questionary
        >>> questionary.date("Type a date: ").ask()
        ? Type a date: 2021-01-01
        '2021-01-01'

    .. _dateparser: https://github.com/scrapinghub/dateparser
    .. _dateutil: https://github.com/dateutil/dateutil
    """
    # delimeter used to separate year, month and day
    if isinstance(date_format, str):
        delimeter: str = date_format[-3]
    else:
        delimeter = " "

    parser = parser or custom_date_parser
    if no_extra_parser:
        parser = None

    merged_style = merge_styles([DEFAULT_STYLE, style])

    if print_date_format:
        rprompt = to_formatted_text(
            f"Date format: {date_format}", style="bg: ansigreen bold"
        )
    else:
        rprompt = None

    def get_prompt_tokens() -> List[Tuple[str, str]]:
        return [("class:qmark", qmark), ("class:question", " {} ".format(message))]

    def _parse_to_date(
        input: str,
    ) -> Union[str, datetime.datetime, datetime.date, None]:
        if return_date_object:
            if parser is not None:
                return parser(input)
            else:
                return datetime.datetime.strptime(input, date_format)  # type: ignore[arg-type]
        else:
            return input

    # set validator
    validate = validate or FullDateValidator(date_format=date_format, parser=parser)
    validator: Validator = build_validator(validate)

    # set completer
    completer = completer or FullDateCompleter(date_format=date_format, parser=parser)

    bindings = KeyBindings()

    # set behavior on `carriage return`
    @bindings.add(Keys.ControlM, eager=True)
    def set_answer(event: KeyPressEvent):
        if event.current_buffer.complete_state is not None:
            event.current_buffer.complete_state = None
        elif event.app.current_buffer.validate(set_cursor=True):
            # When the validation succeeded, accept the input.
            result_date = event.app.current_buffer.document.text
            if result_date.endswith(delimeter):
                result_date = result_date[:-1]

            event.app.exit(result=_parse_to_date(result_date))
            event.app.current_buffer.append_to_history()

    # delimeter should not be placed twice
    @bindings.add(delimeter, eager=True)
    def next_segment(event: KeyPressEvent):
        b = event.app.current_buffer

        if b.complete_state:
            b.complete_state = None

        current_date = b.document.text
        if not current_date.endswith(delimeter):
            b.insert_text(delimeter)

        b.start_completion(select_first=False)

    # initiate ``PromptSession``
    p = PromptSession(
        get_prompt_tokens,
        lexer=SimpleLexer("class:answer"),
        style=merged_style,
        completer=completer,
        validator=validator,
        complete_style=complete_style,
        key_bindings=bindings,
        rprompt=rprompt,
        **kwargs,
    )
    p.default_buffer.reset(Document(default))

    return Question(p.app)
