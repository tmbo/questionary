.PHONY: clean install formatter types

JOBS ?= 1

help:
	@echo "make"
	@echo "    clean"
	@echo "        Remove Python/build artifacts."
	@echo "    install"
	@echo "        Install questionary."
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    types"
	@echo "        Check for type errors using pytype."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf questionary.egg-info/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	rm -rf dist/

install:
	poetry install

formatter:
	poetry run black .

types:
	poetry run mypy questionary
