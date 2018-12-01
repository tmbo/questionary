# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from questionary.prompts import input


def question(message, **kwargs):
    return input.question(message, is_password=True, **kwargs)
