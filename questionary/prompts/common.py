# -*- coding: utf-8 -*-
import inspect
from dataclasses import dataclass

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


class ChoiceClass:
    class_base = "class:"
    pointer = f"{class_base}pointer"
    text = f"{class_base}text"
    separator = f"{class_base}separator"
    selected = f"{class_base}selected"
    highlighted = f"{class_base}highlighted"
    disabled = f"{class_base}disabled"
    set_cursor_position = "[SetCursorPosition]"

    @staticmethod
    def create(name):
        return f"{ChoiceClass.class_base}{name}"


class Choice(object):
    """One choice in a select, rawselect or checkbox."""

    def __init__(
        self,
        title: Text,
        value: Optional[Any] = None,
        disabled: Optional[Text] = None,
        checked: bool = False,
        shortcut_key: Optional[Text] = None,
        style: Optional[Text] = None,
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

            style: Style that this item should use.
        """

        self.disabled = disabled
        self.title = title
        self.checked = checked
        self.style = style

        if value is not None:
            self.value = value
        elif isinstance(title, list):
            self.value = "".join([token[1] for token in title])
        else:
            self.value = title

        self.shortcut_key = str(shortcut_key) if shortcut_key else None

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
                c.get("style", None),
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


class QuestionaryControl(FormattedTextControl):
    SHORTCUT_KEYS = "1,2,3,4,5,6,7,8,9,0,a,b,c,d,ef,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,x,y,z".split(',')

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

        self.is_answered = False
        self.choices = [Choice.build(c) for c in choices]
        self.selected_options = [choice.value for choice in self.choices if self._is_selected(choice)]
        self.pointed_at = self.get_first_valid_choice()
        self._assign_shortcut_keys()

        super(QuestionaryControl, self).__init__(self._get_choice_tokens, **kwargs)

    def _is_selected(self, choice):
        matches_default_value = self.default is not None and choice.value == self.default
        return (matches_default_value or choice.checked) and not choice.disabled

    def _assign_shortcut_keys(self):
        choices_with_assigned_shortcut_key = [c for c in self.choices if c.shortcut_key]
        choices_without_assigned_shortcut_key = [c for c in self.choices if not c.shortcut_key and not c.disabled]

        used_shortcut_keys = []
        for c in choices_with_assigned_shortcut_key:
            valid_shortcut = c.shortcut_key in self.SHORTCUT_KEYS and c.shortcut_key not in used_shortcut_keys
            if not valid_shortcut:
                raise ValueError(
                    f"Invalid shortcut '{c.shortcut_key}'"
                    f"for choice '{c.title}'."
                    "Shortcuts must be unique."
                    f"Valid shortcuts: {', '.join(self.SHORTCUT_KEYS)}"
                )
            used_shortcut_keys.append(c.shortcut_key)

        unused_shortcut_keys = [key for key in self.SHORTCUT_KEYS if key not in used_shortcut_keys]
        for i, c in enumerate(choices_without_assigned_shortcut_key):
            if i == len(unused_shortcut_keys):
                break  # fail gracefully if we run out of shortcuts
            c.shortcut_key = unused_shortcut_keys[i]

    def get_first_valid_choice(self):
        for i, c in enumerate(self.choices):
            if not c.disabled:
                return i
        return None

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, choice):
            selected = choice.value in self.selected_options

            if index == self.pointed_at:
                if self.use_pointer:
                    tokens.append((ChoiceClass.pointer, f" {SELECTED_POINTER} "))
                else:
                    tokens.append((ChoiceClass.text, "   "))

                tokens.append((ChoiceClass.set_cursor_position, ""))
            else:
                if choice.style:
                    tokens.append((ChoiceClass.create(choice.style), "   "))
                else:
                    tokens.append((ChoiceClass.text, "   "))

            if isinstance(choice, Separator):
                tokens.append((ChoiceClass.separator, choice.title))
            elif choice.disabled:
                choice_class = ChoiceClass.selected if selected else ChoiceClass.disabled
                if isinstance(choice.title, list):
                    tokens.append(
                        (choice_class, "- ")
                    )
                    tokens.extend(choice.title)
                else:
                    tokens.append(
                        (choice_class, f"- {choice.title}")
                    )

                disabled_text = f" ({choice.disabled})"
                tokens.append((choice_class, disabled_text))
            else:
                has_valid_shortcut = self.use_shortcuts and choice.shortcut_key is not None
                shortcut = f"{choice.shortcut_key}) " if has_valid_shortcut else ""

                if selected:
                    if self.use_indicator:
                        indicator = INDICATOR_SELECTED + " "
                    else:
                        indicator = ""

                    tokens.append((ChoiceClass.selected, f"{indicator}"))
                else:
                    if self.use_indicator:
                        indicator = INDICATOR_UNSELECTED + " "
                    else:
                        indicator = ""

                    tokens.append((ChoiceClass.text, f"{indicator}"))

                if isinstance(choice.title, list):
                    tokens.extend(choice.title)
                else:
                    title_with_shortcut = f"{shortcut}{choice.title}"

                    if selected:
                        title_class = ChoiceClass.selected
                    elif index == self.pointed_at:
                        title_class = ChoiceClass.highlighted
                    elif choice.style:
                        title_class = ChoiceClass.create(choice.style)
                    else:
                        title_class = ChoiceClass.text
                    tokens.append((title_class, title_with_shortcut))

            tokens.append(("", "\n"))

        # prepare the select choices
        for i, c in enumerate(self.choices):
            append(i, c)

        if self.use_shortcuts:
            tokens.append(
                (
                    ChoiceClass.text,
                    f"  Answer: {self.get_pointed_at().shortcut_key}" "",
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
        return [c for c in self.choices if (not isinstance(c, Separator) and c.value in self.selected_options)]


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
                        message = "invalid input" if verdict is False else verdict
                        raise ValidationError(
                            message=message, cursor_position=len(document.text)
                        )

            return _InputValidator()
    return None


def _fix_unecessary_blank_lines(ps: PromptSession) -> None:
    """This is a fix for additional empty lines added by prompt toolkit.

    This assumes the layout of the default session doesn't change, if it
    does, this needs an update."""

    default_buffer_window = (
        ps.layout.container.get_children()[0].content.get_children()[1].content
    )

    assert isinstance(default_buffer_window, Window)
    # this forces the main window to stay as small as possible, avoiding
    # empty lines in selections
    default_buffer_window.dont_extend_height = Always()


def create_questionary_layout(
    ic: QuestionaryControl,
    get_prompt_tokens: Callable[[], List[Tuple[Text, Text]]],
    **kwargs
) -> Layout:
    """Create a layout combining question and questionary selection."""

    ps = PromptSession(get_prompt_tokens, reserve_space_for_menu=0, **kwargs)

    _fix_unecessary_blank_lines(ps)

    return Layout(
        HSplit(
            [ps.layout.container, ConditionalContainer(Window(ic), filter=~IsDone())]
        )
    )
