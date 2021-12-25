import questionary


def main():
    while True:
        x = questionary.password("Password").ask()
        y = questionary.password("Repeat password").ask()

        if x == y:
            print(x)
            break

        else:
            print("Passwords do not match. Try again.")


if __name__ == "__main__":
    main()
