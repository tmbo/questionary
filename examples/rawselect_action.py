import questionary

if __name__ == "__main__":
    action = (
        questionary.rawselect(
            "What do you want to do?",
            choices=["Order a pizza", "Make a reservation", "Ask for opening hours"],
        ).ask()
        or "do nothing"
    )

    print(f"Sorry, I can't {action}. Bye! 🙅")
