import questionary

if __name__ == "__main__":
    import questionary

    answers = questionary.form(
        first=questionary.confirm("Would you like the next question?", default=True),
        second=questionary.select("Select item", choices=["item1", "item2", "item3"])
    ).ask()

    print(answers)
