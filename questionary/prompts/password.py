# -*- coding: utf-8 -*-
from questionary.prompts import input


def question(message, **kwargs):
    return input.question(message, is_password=True, **kwargs)
