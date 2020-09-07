import questionary

if __name__ == "__main__":
    name = questionary.text("What's your first name").ask()
    print(f"Hey {name} 🦄")
