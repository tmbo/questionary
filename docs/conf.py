import os
import sys

sys.path.insert(0, os.path.abspath("../"))
from questionary import __version__  # noqa: E402

project = "Questionary"
copyright = "2021, Questionary"
author = "Questionary"

version = __version__
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
]

autodoc_typehints = "description"

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "navigation_depth": 2,
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "prompt_toolkit": ("https://python-prompt-toolkit.readthedocs.io/en/3.0.36/", None),
}

autodoc_member_order = "alphabetical"
