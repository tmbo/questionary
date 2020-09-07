import questionary

if __name__ == "__main__":
    password = questionary.password("What's your secret?").ask() or ""

    print(
        f"Your secret is {password[:1]}... no just kidding - "
        f"I'm not going to tell anyone. 🤫"
    )
