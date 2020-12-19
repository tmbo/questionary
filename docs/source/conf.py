import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from questionary import __version__

project = "Questionary"
copyright = "2020, Questionary"
author = "Questionary"

version = __version__
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

html_theme = "sphinx_rtd_theme"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "prompt_toolkit": ("https://python-prompt-toolkit.readthedocs.io/en/master/", None),
}

autodoc_member_order = "alphabetical"
