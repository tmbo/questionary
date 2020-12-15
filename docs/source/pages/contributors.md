# Contributor's Guide

## Steps for Submitting Code
Contributions are very much welcomed and appreciated. Every little bit of help
counts, so do not hesitate!

1. Check for open issues, or open a new issue to start some discussion around a
   feature idea or bug. There is a [Contributor Friendly](https://github.com/tmbo/questionary/issues?direction=desc&labels=good+first+issue&page=1&sort=upd)
   tag for issues that should be ideal for people who are not familiar with the codebase yet.

2. Fork [the repository](https://github.com/tmbo/questionary) on GitHub to start
   making your changes.

3. Write some tests that show the bug is fixed or that the feature works as expected.

4. Ensure your code passes the style checks by running `black questionary`.

5. Check all of the unit tests pass by running `pytest --pycodestyle --cov questionary -v`.

6. Check the type checks pass by running `mypy questionary`.

7. Send a pull request and bug the maintainer until it gets merged and
   published 🙂

## Bug Reports
Bug reports should be page to the [issue tracker](https://github.com/tmbo/questionary/issues).

## Feature Requests
Feature requests should be page to the [issue tracker](https://github.com/tmbo/questionary/issues).

## Other
### Create a New Release

1. Update the version number in `questionary/version.py` and `pyproject.toml`.
2. Add a new section for the release to the changelog [here](https://github.com/tmbo/questionary).
3. Commit these changes.
4. `git tag` the commit with the release version number.

GitHub Actions will build and push the updated library to PyPi.

### Create a Command Line Recording

1. Install `brew install asciinema` and `npm install --global asciicast2gif`.
2. Run `asciinema rec`.
3. Do the thing.
4. Convert to gif `asciicast2gif -h 7 -w 120 -s 2 <recoding> output.gif`.
