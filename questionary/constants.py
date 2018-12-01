# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
