import inspect
from prompt_toolkit import PromptSession
from prompt_toolkit.filters import IsDone, Always, Condition
from prompt_toolkit.layout import (
    FormattedTextControl,
    Layout,
    HSplit,
    ConditionalContainer,
    Window,
)
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.validation import Validator, ValidationError
from typing import Optional, Any, List, Dict, Union, Callable, Sequence, Tuple

from questionary.constants import (
    DEFAULT_STYLE,
    SELECTED_POINTER,
    INDICATOR_SELECTED,
    INDICATOR_UNSELECTED,
    INVALID_INPUT,
)

# This is a cut-down version of `prompt_toolkit.formatted_text.AnyFormattedText`
# which does not exist in v2 of prompt_toolkit
FormattedText = Union[
    str,
    List[Tuple[str, str]],
    List[Tuple[str, str, Callable[[Any], None]]],
    None,
]


class Choice:
    """One choice in a :meth:`select`, :meth:`rawselect` or :meth:`checkbox`.

    Args:
        title: Text shown in the selection list.

        value: Value returned, when the choice is selected.

        disabled: If set, the choice can not be selected by the user. The
                  provided text is used to explain, why the selection is
                  disabled.

        checked: Preselect this choice when displaying the options.

        shortcut_key: Key shortcut used to select this item.
    """

    title: FormattedText
    """Dispay string for the choice"""

    value: Optional[Any]
    """Value of the choice"""

    disabled: Optional[str]
    """Whether the choice can be selected"""

    checked: Optional[bool]
    """Whether the choice is initially selected"""

    shortcut_key: Optional[str]
    """A shortcut key for the choice"""

    def __init__(
        self,
        title: FormattedText,
        value: Optional[Any] = None,
        disabled: Optional[str] = None,
        checked: Optional[bool] = False,
        shortcut_key: Optional[str] = None,
    ) -> None:

        self.disabled = disabled
        self.title = title
        self.checked = checked if checked is not None else False

        if value is not None:
            self.value = value
        elif isinstance(title, list):
            self.value = "".join([token[1] for token in title])
        else:
            self.value = title

        if shortcut_key is not None:
            self.shortcut_key = str(shortcut_key)
        else:
            self.shortcut_key = None

    @staticmethod
    def build(c: Union[str, "Choice", Dict[str, Any]]) -> "Choice":
        """Create a choice object from different representations.

        Args:
            c: Either a :obj:`str`, :class:`Choice` or :obj:`dict` with
               ``name``, ``value``, ``disabled``, ``checked`` and
               ``key`` properties.

        Returns:
            An instance of the :class:`Choice` object.
        """

        if isinstance(c, Choice):
            return c
        elif isinstance(c, str):
            return Choice(c, c)
        else:
            return Choice(
                c.get("name"),
                c.get("value"),
                c.get("disabled", None),
                c.get("checked"),
                c.get("key"),
            )


class Separator(Choice):
    """Used to space/separate choices group."""

    default_separator: str = "-" * 15
    """The default seperator used if none is specified"""

    line: str
    """The string being used as a seperator"""

    def __init__(self, line: Optional[str] = None) -> None:
        """Create a separator in a list.

        Args:
            line: Text to be displayed in the list, by default uses ``---``.
        """

        self.line = line or self.default_separator
        super().__init__(self.line, None, "-")


class InquirerControl(FormattedTextControl):
    SHORTCUT_KEYS = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    choices: List[Choice]
    default: Optional[Union[str, Choice, Dict[str, Any]]]
    selected_options: List[Any]
    use_indicator: bool
    use_shortcuts: bool
    use_arrow_keys: bool
    use_pointer: bool
    pointed_at: int
    is_answered: bool

    def __init__(
        self,
        choices: Sequence[Union[str, Choice, Dict[str, Any]]],
        default: Optional[Union[str, Choice, Dict[str, Any]]] = None,
        use_indicator: bool = True,
        use_shortcuts: bool = False,
        use_arrow_keys: bool = True,
        use_pointer: bool = True,
        initial_choice: Optional[Union[str, Choice, Dict[str, Any]]] = None,
        **kwargs: Any,
    ):

        self.use_indicator = use_indicator
        self.use_shortcuts = use_shortcuts
        self.use_arrow_keys = use_arrow_keys
        self.use_pointer = use_pointer
        self.default = default

        if default is not None and default not in choices:
            raise ValueError(
                f"Invalid `default` value passed. The value (`{default}`) "
                f"does not exist in the set of choices. Please make sure the "
                f"default value is one of the available choices."
            )

        if initial_choice is None:
            pointed_at = None
        elif initial_choice in choices:
            pointed_at = choices.index(initial_choice)
        else:
            raise ValueError(
                f"Invalid `initial_choice` value passed. The value "
                f"(`{initial_choice}`) does not exist in "
                f"the set of choices. Please make sure the initial value is "
                f"one of the available choices."
            )

        self.is_answered = False
        self.choices = []
        self.submission_attempted = False
        self.error_message = None
        self.selected_options = []

        self._init_choices(choices, pointed_at)
        self._assign_shortcut_keys()

        super().__init__(self._get_choice_tokens, **kwargs)

        if not self.is_selection_valid():
            raise ValueError(
                f"Invalid 'initial_choice' value ('{initial_choice}'). "
                f"It must be a selectable value."
            )

    def _is_selected(self, choice: Choice):
        return (
            choice.checked or choice.value == self.default and self.default is not None
        ) and not choice.disabled

    def _assign_shortcut_keys(self):
        available_shortcuts = self.SHORTCUT_KEYS[:]

        # first, make sure we do not double assign a shortcut
        for c in self.choices:
            if c.shortcut_key is not None:
                if c.shortcut_key in available_shortcuts:
                    available_shortcuts.remove(c.shortcut_key)
                else:
                    raise ValueError(
                        "Invalid shortcut '{}'"
                        "for choice '{}'. Shortcuts "
                        "should be single characters or numbers. "
                        "Make sure that all your shortcuts are "
                        "unique.".format(c.shortcut_key, c.title)
                    )

        shortcut_idx = 0
        for c in self.choices:
            if c.shortcut_key is None and not c.disabled:
                c.shortcut_key = available_shortcuts[shortcut_idx]
                shortcut_idx += 1

            if shortcut_idx == len(available_shortcuts):
                break  # fail gracefully if we run out of shortcuts

    def _init_choices(
        self,
        choices: Sequence[Union[str, Choice, Dict[str, Any]]],
        pointed_at: Optional[int],
    ):
        # helper to convert from question format to internal format
        self.choices = []

        if pointed_at is not None:
            self.pointed_at = pointed_at

        for i, c in enumerate(choices):
            choice = Choice.build(c)

            if self._is_selected(choice):
                self.selected_options.append(choice.value)

            if pointed_at is None and not choice.disabled:
                # find the first (available) choice
                self.pointed_at = pointed_at = i

            self.choices.append(choice)

    @property
    def choice_count(self) -> int:
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index: int, choice: Choice):
            # use value to check if option has been selected
            selected = choice.value in self.selected_options

            if index == self.pointed_at:
                if self.use_pointer:
                    tokens.append(("class:pointer", " {} ".format(SELECTED_POINTER)))
                else:
                    tokens.append(("class:text", "   "))

                tokens.append(("[SetCursorPosition]", ""))
            else:
                tokens.append(("class:text", "   "))

            if isinstance(choice, Separator):
                tokens.append(("class:separator", "{}".format(choice.title)))
            elif choice.disabled:  # disabled
                if isinstance(choice.title, list):
                    tokens.append(
                        ("class:selected" if selected else "class:disabled", "- ")
                    )
                    tokens.extend(choice.title)
                else:
                    tokens.append(
                        (
                            "class:selected" if selected else "class:disabled",
                            "- {}".format(choice.title),
                        )
                    )

                tokens.append(
                    (
                        "class:selected" if selected else "class:disabled",
                        "{}".format(
                            ""
                            if isinstance(choice.disabled, bool)
                            else " ({})".format(choice.disabled)
                        ),
                    )
                )
            else:
                if self.use_shortcuts and choice.shortcut_key is not None:
                    shortcut = "{}) ".format(choice.shortcut_key)
                else:
                    shortcut = ""

                if selected:
                    if self.use_indicator:
                        indicator = INDICATOR_SELECTED + " "
                    else:
                        indicator = ""

                    tokens.append(("class:selected", "{}".format(indicator)))
                else:
                    if self.use_indicator:
                        indicator = INDICATOR_UNSELECTED + " "
                    else:
                        indicator = ""

                    tokens.append(("class:text", "{}".format(indicator)))

                if isinstance(choice.title, list):
                    tokens.extend(choice.title)
                elif selected:
                    tokens.append(
                        ("class:selected", "{}{}".format(shortcut, choice.title))
                    )
                elif index == self.pointed_at:
                    tokens.append(
                        ("class:highlighted", "{}{}".format(shortcut, choice.title))
                    )
                else:
                    tokens.append(("class:text", "{}{}".format(shortcut, choice.title)))

            tokens.append(("", "\n"))

        # prepare the select choices
        for i, c in enumerate(self.choices):
            append(i, c)

        if self.use_shortcuts:
            tokens.append(
                (
                    "class:text",
                    "  Answer: {}" "".format(self.get_pointed_at().shortcut_key),
                )
            )
        else:
            tokens.pop()  # Remove last newline.
        return tokens

    def is_selection_a_separator(self) -> bool:
        selected = self.choices[self.pointed_at]
        return isinstance(selected, Separator)

    def is_selection_disabled(self) -> Optional[str]:
        return self.choices[self.pointed_at].disabled

    def is_selection_valid(self) -> bool:
        return not self.is_selection_disabled() and not self.is_selection_a_separator()

    def select_previous(self) -> None:
        self.pointed_at = (self.pointed_at - 1) % self.choice_count

    def select_next(self) -> None:
        self.pointed_at = (self.pointed_at + 1) % self.choice_count

    def get_pointed_at(self) -> Choice:
        return self.choices[self.pointed_at]

    def get_selected_values(self) -> List[Choice]:
        # get values not labels
        return [
            c
            for c in self.choices
            if (not isinstance(c, Separator) and c.value in self.selected_options)
        ]


def build_validator(validate: Any) -> Optional[Validator]:
    if validate:
        if inspect.isclass(validate) and issubclass(validate, Validator):
            return validate()
        elif isinstance(validate, Validator):
            return validate
        elif callable(validate):

            class _InputValidator(Validator):
                def validate(self, document):
                    verdict = validate(document.text)
                    if verdict is not True:
                        if verdict is False:
                            verdict = INVALID_INPUT
                        raise ValidationError(
                            message=verdict, cursor_position=len(document.text)
                        )

            return _InputValidator()
    return None


def _fix_unecessary_blank_lines(ps: PromptSession) -> None:
    """This is a fix for additional empty lines added by prompt toolkit.

    This assumes the layout of the default session doesn't change, if it
    does, this needs an update."""

    default_container = ps.layout.container

    default_buffer_window = (
        default_container.get_children()[0].content.get_children()[1].content
    )

    assert isinstance(default_buffer_window, Window)
    # this forces the main window to stay as small as possible, avoiding
    # empty lines in selections
    default_buffer_window.dont_extend_height = Always()
    default_buffer_window.always_hide_cursor = Always()


def create_inquirer_layout(
    ic: InquirerControl,
    get_prompt_tokens: Callable[[], List[Tuple[str, str]]],
    **kwargs: Any,
) -> Layout:
    """Create a layout combining question and inquirer selection."""

    ps = PromptSession(get_prompt_tokens, reserve_space_for_menu=0, **kwargs)
    _fix_unecessary_blank_lines(ps)

    validation_prompt = PromptSession(bottom_toolbar=lambda: ic.error_message, **kwargs)

    return Layout(
        HSplit(
            [
                ps.layout.container,
                ConditionalContainer(Window(ic), filter=~IsDone()),
                ConditionalContainer(
                    validation_prompt.layout.container,
                    filter=Condition(lambda: ic.error_message is not None),
                ),
            ]
        )
    )


def print_formatted_text(text: str, style: Optional[str] = None, **kwargs: Any) -> None:
    """Print formatted text.

    Sometimes you want to spice up your printed messages a bit,
    :meth:`questionary.print` is a helper to do just that.

    Example:

        >>> import questionary
        >>> questionary.print("Hello World 🦄", style="bold italic fg:darkred")
        Hello World 🦄

    .. image:: ../images/print.gif

    Args:
        text: Text to be printed.
        style: Style used for printing. The style argument uses the
            prompt :ref:`toolkit style strings <prompt_toolkit:styling>`.
    """
    from prompt_toolkit import print_formatted_text as pt_print
    from prompt_toolkit.formatted_text import FormattedText as FText

    if style is not None:
        text_style = Style([("text", style)])
    else:
        text_style = DEFAULT_STYLE

    pt_print(FText([("class:text", text)]), style=text_style, **kwargs)
