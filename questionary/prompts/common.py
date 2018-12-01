# -*- coding: utf-8 -*-
"""
common prompt functionality
"""

import sys

from prompt_toolkit.validation import Validator, ValidationError

PY3 = sys.version_info[0] >= 3

if PY3:
    basestring = str


class Separator(object):
    """Used to space/separate choices group"""

    line = '-' * 15

    def __init__(self, line=None):
        if line:
            self.line = line

    @property
    def title(self):
        return self.line

    @property
    def value(self):
        return None

    @property
    def disabled(self):
        return True

    def __str__(self):
        return self.line


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
                    #print('validation!!')
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
        raise ValueError('Here a simple validate function is expected, no class')

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
