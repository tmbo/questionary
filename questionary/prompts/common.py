# -*- coding: utf-8 -*-
"""
common prompt functionality
"""

import sys

from prompt_toolkit.layout import FormattedTextControl
from prompt_toolkit.validation import Validator, ValidationError

from questionary.constants import (SELECTED_POINTER, INDICATOR_SELECTED,
                                   INDICATOR_UNSELECTED)

PY3 = sys.version_info[0] >= 3

if PY3:
    basestring = str


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

    def __str__(self):
        return self.line


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
                if isinstance(c, basestring):
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

    @property
    def line_count(self):
        return len(self.choices)


# TODO probably better to use base.Condition
def setup_validator(kwargs):
    # this is an internal helper not meant for public consumption!
    # note this works on a dictionary
    validate_prompt = kwargs.pop('validate', None)
    if validate_prompt:
        if issubclass(validate_prompt, Validator):
            kwargs['validator'] = validate_prompt()
        elif callable(validate_prompt):
            class _InputValidator(Validator):
                def validate(self, document):
                    # print('validation!!')
                    verdict = validate_prompt(document.text)
                    if isinstance(verdict, basestring):
                        raise ValidationError(
                            message=verdict,
                            cursor_position=len(document.text))
                    elif verdict is not True:
                        raise ValidationError(
                            message='invalid input',
                            cursor_position=len(document.text))

            kwargs['validator'] = _InputValidator()
        return kwargs['validator']


def setup_simple_validator(kwargs):
    # this is an internal helper not meant for public consumption!
    # note this works on a dictionary
    # this validates the answer not a buffer
    # TODO
    # not sure yet how to deal with the validation result:
    # https://github.com/jonathanslenders/python-prompt-toolkit/issues/430
    validate = kwargs.pop('validate', None)
    if validate is None:
        def _always(answer):
            return True

        return _always
    elif not callable(validate):
        raise ValueError('Here a simple validate function is '
                         'expected, no class')

    def _validator(answer):
        verdict = validate(answer)
        if isinstance(verdict, basestring):
            raise ValidationError(
                message=verdict
            )
        elif verdict is not True:
            raise ValidationError(
                message='invalid input'
            )

    return _validator
