import questionary

if __name__ == "__main__":
    action = (
        questionary.select(
            "Press Left/Right arraw keys or PageUp/PageDown or h/l(vim mode) to move one page",
            choices=[str(x) for x in range(200)],
        ).ask()
        or "do nothing"
    )

    print(f"Selected {action}. Bye! 👋")
