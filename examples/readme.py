# Asyncio bug workaround
# https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1023
import asyncio
import selectors

selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
# End workaround

import questionary
from examples import custom_style_dope

if __name__ == "__main__":
    questionary.text("What's your first name").ask()
    questionary.password("What's your secret?").ask()
    questionary.confirm("Are you amazed?").ask()
    questionary.select(
        "What do you want to do?",
        choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
    ).ask()
    questionary.rawselect(
        "What do you want to do?",
        choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
    ).ask()
    questionary.checkbox(
        "Select toppings", choices=["foo", "bar", "bazz"], style=custom_style_dope
    ).ask()
    questionary.path("Path to the projects version file").ask()
