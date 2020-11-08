from questionary.prompts import autocomplete
from questionary.prompts import confirm
from questionary.prompts import text
from questionary.prompts import select
from questionary.prompts import rawselect
from questionary.prompts import password
from questionary.prompts import checkbox
from questionary.prompts import path

AVAILABLE_PROMPTS = {
    "autocomplete": autocomplete.autocomplete,
    "confirm": confirm.confirm,
    "text": text.text,
    "select": select.select,
    "rawselect": rawselect.rawselect,
    "password": password.password,
    "checkbox": checkbox.checkbox,
    "path": path.path,
    # backwards compatible names
    "list": select.select,
    "rawlist": rawselect.rawselect,
    "input": text.text,
}


def prompt_by_name(name):
    return AVAILABLE_PROMPTS.get(name)
