import questionary

if __name__ == "__main__":
    confirmation = questionary.confirm("Are you amazed?").ask()

    if confirmation:
        print("That is amazing! 💥🚀")
    else:
        print("Tha is unfortunate 🐡.")
