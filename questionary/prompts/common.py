# -*- coding: utf-8 -*-
import inspect
from prompt_toolkit import PromptSession
from prompt_toolkit.filters import IsDone, Always
from prompt_toolkit.layout import (
    FormattedTextControl,
    Layout,
    HSplit,
    ConditionalContainer,
    Window,
)
from prompt_toolkit.validation import Validator, ValidationError
from typing import Optional, Any, List, Text, Dict, Union, Callable, Tuple

from questionary.constants import (
    SELECTED_POINTER,
    INDICATOR_SELECTED,
    INDICATOR_UNSELECTED,
)


class Choice(object):
    """One choice in a select, rawselect or checkbox."""

    def __init__(
        self,
        title: Text,
        value: Optional[Any] = None,
        disabled: Optional[Text] = None,
        checked: bool = False,
        shortcut_key: Optional[Text] = None,
    ) -> None:
        """Create a new choice.

        Args:
            title: Text shown in the selection list.

            value: Value returned, when the choice is selected.

            disabled: If set, the choice can not be selected by the user. The
                      provided text is used to explain, why the selection is
                      disabled.

            checked: Preselect this choice when displaying the options.

            shortcut_key: Key shortcut used to select this item.
        """

        self.disabled = disabled
        self.title = title
        self.checked = checked

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
    def build(c: Union[Text, "Choice", Dict[Text, Any]]) -> "Choice":
        """Create a choice object from different representations."""

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

    default_separator = "-" * 15

    def __init__(self, line: Optional[Text] = None):
        """Create a separator in a list.

        Args:
            line: Text to be displayed in the list, by default uses `---`.
        """

        self.line = line or self.default_separator
        super(Separator, self).__init__(self.line, None, "-")


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

    def __init__(
        self,
        choices: List[Union[Text, Choice, Dict[Text, Any]]],
        default: Optional[Any] = None,
        use_indicator: bool = True,
        use_shortcuts: bool = False,
        use_pointer: bool = True,
        **kwargs
    ):

        self.use_indicator = use_indicator
        self.use_shortcuts = use_shortcuts
        self.use_pointer = use_pointer
        self.default = default

        self.pointed_at = None
        self.is_answered = False
        self.choices = []
        self.selected_options = []

        self._init_choices(choices)
        self._assign_shortcut_keys()

        super(InquirerControl, self).__init__(self._get_choice_tokens, **kwargs)

    def _is_selected(self, choice):
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

    def _init_choices(self, choices):
        # helper to convert from question format to internal format
        self.choices = []

        for i, c in enumerate(choices):
            choice = Choice.build(c)

            if self._is_selected(choice):
                self.selected_options.append(choice.value)

            if self.pointed_at is None and not choice.disabled:
                # find the first (available) choice
                self.pointed_at = i

            self.choices.append(choice)

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, choice):
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

    def is_selection_a_separator(self):
        selected = self.choices[self.pointed_at]
        return isinstance(selected, Separator)

    def is_selection_disabled(self):
        return self.choices[self.pointed_at].disabled

    def is_selection_valid(self):
        return not self.is_selection_disabled() and not self.is_selection_a_separator()

    def select_previous(self):
        self.pointed_at = (self.pointed_at - 1) % self.choice_count

    def select_next(self):
        self.pointed_at = (self.pointed_at + 1) % self.choice_count

    def get_pointed_at(self):
        return self.choices[self.pointed_at]

    def get_selected_values(self):
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
                            verdict = "invalid input"
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


def create_inquirer_layout(
    ic: InquirerControl,
    get_prompt_tokens: Callable[[], List[Tuple[Text, Text]]],
    **kwargs
) -> Layout:
    """Create a layout combining question and inquirer selection."""

    ps = PromptSession(get_prompt_tokens, reserve_space_for_menu=0, **kwargs)

    _fix_unecessary_blank_lines(ps)

    return Layout(
        HSplit(
            [ps.layout.container, ConditionalContainer(Window(ic), filter=~IsDone())]
        )
    )
