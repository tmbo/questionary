import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from questionary import __version__

project = "Questionary"
copyright = "2020, Questionary"
author = "Questionary"

release = __version__

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

html_theme = "sphinx_rtd_theme"

intersphinx_mapping = {
    "https://docs.python.org/": None,
    "prompt_toolkit": ("https://python-prompt-toolkit.readthedocs.io/en/master/", None),
}

autosectionlabel_prefix_document = True
