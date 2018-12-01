# -*- coding: utf-8 -*-
from prompt_toolkit.layout import FormattedTextControl
from prompt_toolkit.validation import Validator, ValidationError

from questionary.constants import (SELECTED_POINTER, INDICATOR_SELECTED,
                                   INDICATOR_UNSELECTED)


class Choice(object):

    def __init__(self, title, value, disabled):
        self.disabled = disabled
        self.value = value
        self.title = title


class Separator(Choice):
    """Used to space/separate choices group"""

    line = '-' * 15

    def __init__(self, line=None):
        if line:
            self.line = line
        super(Separator, self).__init__(self.line, None, True)


class InquirerControl(FormattedTextControl):
    def __init__(self, choices, default, use_indicator=True, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.use_indicator = use_indicator
        self.default = default
        self.choices = []  # type: List[Choice]
        self.selected_options = []  # list of names
        self._init_choices(choices, default)
        super(InquirerControl, self).__init__(self._get_choice_tokens,
                                              **kwargs)

    def _is_selected(self, checked, choice):
        return ((checked or choice.value == self.default and
                 self.default is not None) and
                not choice.disabled)

    def _init_choices(self, choices, default=None):
        # helper to convert from question format to internal format
        self.choices = []  # list (name, value, disabled)
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                choice = c
            else:
                if isinstance(c, str):
                    choice = Choice(c, c, False)
                else:
                    choice = Choice(c.get('name'),
                                    c.get('value', c.get('name')),
                                    c.get('disabled', None))
                    if self._is_selected(c.get('checked'), choice):
                        self.selected_options.append(choice.value)

                if searching_first_choice and not choice.disabled:
                    # find the first (available) choice
                    self.selected_option_index = i
                    searching_first_choice = False

            self.choices.append(choice)

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, choice):
            # use value to check if option has been selected
            selected = (choice.value in self.selected_options)
            pointed_at = (index == self.selected_option_index)

            if pointed_at:
                tokens.append(("class:pointer",
                               ' {} '.format(SELECTED_POINTER)))
                tokens.append(('[SetCursorPosition]', ''))
            else:
                tokens.append(("", '   '))

            if isinstance(choice, Separator):
                tokens.append(("class:separator",
                               "{}".format(choice.title)))
            elif choice.disabled:  # disabled
                tokens.append(("class:selected" if selected else "",
                               '- {} ({})'.format(choice.title,
                                                  choice.disabled)))
            else:
                if selected:
                    if self.use_indicator:
                        indicator = INDICATOR_SELECTED + " "
                    else:
                        indicator = ""
                    tokens.append(("class:selected",
                                   "{}{}".format(indicator, choice.title)))
                else:
                    if self.use_indicator:
                        indicator = INDICATOR_UNSELECTED + " "
                    else:
                        indicator = ""

                    tokens.append(("",
                                   "{}{}".format(indicator, choice.title)))

            tokens.append(("", '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def is_selection_a_separator(self):
        selected = self.choices[self.selected_option_index]
        return isinstance(selected, Separator)

    def is_selection_disabled(self):
        return self.choices[self.selected_option_index].disabled

    def is_selection_valid(self):
        return (not self.is_selection_disabled() and
                not self.is_selection_a_separator())

    def select_previous(self):
        self.selected_option_index = (
                (self.selected_option_index - 1) % self.choice_count)

    def select_next(self):
        self.selected_option_index = (
                (self.selected_option_index + 1) % self.choice_count)

    def get_pointed_at(self):
        return self.choices[self.selected_option_index]

    def get_selected_values(self):
        # get values not labels
        return [c
                for c in self.choices
                if (not isinstance(c, Separator) and
                    c.value in self.selected_options)]
