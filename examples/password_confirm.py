import questionary


def create_password(**kwargs):
    x = questionary.password("Password", **kwargs).ask()
    y = questionary.password("Repeat password", **kwargs).ask()

    if x == y:
        questionary.print("✅ ")
        return x

    else:
        questionary.print(
            "Passwords do not match. Try again.", style="italic fg:darkred"
        )
        # until passwords match, we keep repeating the question
        return create_password(**kwargs)


if __name__ == "__main__":
    create_password()
