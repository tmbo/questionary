# -*- coding: utf-8 -*-

from prompt_toolkit.styles import Style

YES = "Yes"

NO = "No"

YES_OR_NO = "(Y/n)"

NO_OR_YES = "(y/N)"

SELECTED_POINTER = "»"

INDICATOR_SELECTED = "●"

INDICATOR_UNSELECTED = "○"

DEFAULT_STYLE = Style([
    ('qmark', 'fg:#5f819d'),
    ('question', 'bold'),
    ('answer', 'fg:#FF9D00 bold'),
    ('pointer', ''),
    ('selected', ''),
    ('separator', ''),
])
