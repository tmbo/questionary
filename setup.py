from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open("questionary/version.py") as f:
    exec(f.read())

# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

tests_requires = [
    "pytest~=4.0",
    "pytest-pycodestyle~=1.3",
    "pytest-cov~=2.6",
    "coveralls~=1.3",
]

install_requires = ["prompt_toolkit>=2.0,<4.0"]

extras_requires = {"test": tests_requires}

setup(
    name="questionary",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    version=__version__,
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require=extras_requires,
    include_package_data=True,
    description="Python library to build pretty command line user prompts ⭐️",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tom Bocklisch",
    author_email="tombocklisch@gmail.com",
    maintainer="Tom Bocklisch",
    maintainer_email="tombocklisch@gmail.com",
    license="MIT",
    keywords="cli ui inquirer questions prompt",
    url="https://github.com/tmbo/questionary",
    download_url="https://github.com/tmbo/questionary/archive/{}.tar.gz"
    "".format(__version__),
    project_urls={
        "Bug Reports": "https://github.com/tmbo/questionary/issues",
        "Source": "https://github.com/tmbo/questionary",
    },
)
