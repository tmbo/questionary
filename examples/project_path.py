import questionary

if __name__ == "__main__":
    path = questionary.path("Path to the projects version file").ask()
    if path:
        print(f"Found version file at {path} 🦄")
    else:
        print("No version file it is then!")
