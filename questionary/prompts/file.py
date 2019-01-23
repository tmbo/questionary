# -*- coding: utf-8 -*-
import errno
import sys

import os
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator, ValidationError
from questionary.constants import (
    DEFAULT_QUESTION_PREFIX,
    DEFAULT_PATH_ERROR)
from questionary.prompts import text
from questionary.question import Question
from typing import Text, Optional, Any


class PathValidator(Validator):
    def __init__(self, should_exist=None, expanduser=True, message=None):
        self.should_exist = should_exist
        self.expanduser = expanduser
        self.message = message or DEFAULT_PATH_ERROR

    @staticmethod
    def is_pathname_valid(pathname: str) -> bool:
        """True if the pathname is valid for the current OS"""
        # If this pathname is either not a string or is but is empty,
        # this pathname
        # is invalid.
        try:
            if not isinstance(pathname, str) or not pathname:
                return False

            # Strip this pathname's Windows-specific drive specifier (e.g.,
            # `C:\`)
            # if any. Since Windows prohibits path components from containing
            # `:`
            # characters, failing to strip this `:`-suffixed prefix would
            # erroneously invalidate all valid absolute Windows pathnames.
            _, pathname = os.path.splitdrive(pathname)

            # Directory guaranteed to exist. If the current OS is Windows,
            # this is
            # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
            # environment variable); else, the typical root directory.
            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)  # ...Murphy and her ironclad Law

            # Append a path separator to this directory if needed.
            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

            # Test whether each path component split from this pathname is
            # valid or
            # not, ignoring non-existent and non-readable path components.
            for pathname_part in pathname.split(os.path.sep):
                try:
                    os.lstat(root_dirname + pathname_part)
                # If an OS-specific exception is raised, its error code
                # indicates whether this pathname is valid or not. Unless this
                # is the case, this exception implies an ignorable kernel or
                # filesystem complaint (e.g., path not found or inaccessible).
                #
                # Only the following exceptions indicate invalid pathnames:
                #
                # * Instances of the Windows-specific "WindowsError" class
                #   defining the "winerror" attribute whose value is
                #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
                #   fine-grained and hence useful than the generic "errno"
                #   attribute. When a too-long pathname is passed, for example,
                #   "errno" is "ENOENT" (i.e., no such file or directory) rather
                #   than "ENAMETOOLONG" (i.e., file name too long).
                # * Instances of the cross-platform "OSError" class defining the
                #   generic "errno" attribute whose value is either:
                #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
                #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == 123:  # invalid name
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        # If a "TypeError" exception was raised, it almost certainly has the
        # error message "embedded NUL character" indicating an invalid pathname.
        except TypeError:
            return False
        except ValueError:
            return False
        # If no exception was raised, all path components and hence this
        # pathname itself are valid. (Praise be to the curmudgeonly python.)
        else:
            return True
        # If any other exception was raised, this is an unrelated fatal issue
        # (e.g., a bug). Permit this exception to unwind the call stack.
        #
        # Did we mention this should be shipped with Python already?

    @staticmethod
    def is_path_creatable(pathname: str) -> bool:
        """Check if there are enough permissions to create the path."""

        # Parent directory of the passed path. If empty, we substitute the
        # current
        # working directory (CWD) instead.
        dirname = os.path.dirname(pathname) or os.getcwd()
        return os.access(dirname, os.W_OK)

    @staticmethod
    def is_path_exists_or_creatable(pathname: str, should_exist: bool) -> bool:
        """Checks if the passed pathname is a valid pathname for the current OS.

        Either the path currently exists or it is hypothetically creatable;
        This function is guaranteed to _never_ raise exceptions."""

        try:
            # To prevent "os" module calls from raising undesirable
            # exceptions on
            # invalid pathnames, is_pathname_valid() is explicitly called first.
            is_valid = PathValidator.is_pathname_valid(pathname)

            if not is_valid:
                return False

            if os.path.exists(pathname):
                return True

            if not should_exist and PathValidator.is_path_creatable(pathname):
                return True

            return False
        # Report failure on non-fatal filesystem complaints (e.g., connection
        # timeouts, permissions issues) implying this path to be
        # inaccessible. All
        # other exceptions are unrelated fatal issues and should not be
        # caught here.
        except OSError:
            return False

    def validate(self, document):
        """Validates that the input is a valid path."""

        if self.expanduser:
            path = os.path.expanduser(document.text)
        else:
            path = document.text

        is_valid = self.is_path_exists_or_creatable(path, self.should_exist)

        if not is_valid:
            raise ValidationError(message=self.message,
                                  cursor_position=len(document.text))


def file(message: Text,
         default: Text = "",
         should_exist: Optional[bool] = None,
         expanduser: bool = True,
         qmark: Text = DEFAULT_QUESTION_PREFIX,
         style: Optional[Style] = None,
         **kwargs: Any) -> Question:
    """Prompt the user to enter a file path.

       This question type can be used to prompt the user for a file path.

       Args:
           message: Question text

           default: Default value will be returned if the user just hits
                    enter.

           should_exist: Validate if the path exists or does not exist. If
                         set to `True`, the path needs to exist. If
                         set to `False`, the path is not allowed to exist. If
                         set to `None`, no check is done.

           qmark: Question prefix displayed in front of the question.
                  By default this is a `?`

           style: A custom color and style for the question parts. You can
                  configure colors as well as font types for different elements.

       Returns:
           Question: Question instance, ready to be prompted (using `.ask()`).
    """

    validate = PathValidator(should_exist, expanduser)

    if expanduser:
        post_process = os.path.expanduser
    else:
        post_process = lambda x: x

    return text.text(message, default, validate, qmark, style, post_process,
                     completer=PathCompleter(expanduser=expanduser),
                     complete_style=CompleteStyle.READLINE_LIKE,
                     **kwargs)
