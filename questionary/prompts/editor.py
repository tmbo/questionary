# -*- coding: utf-8 -*-
import io
import os
import subprocess
import sys
import tempfile

from prompt_toolkit import PromptSession
from prompt_toolkit.document import Document
from prompt_toolkit.styles import merge_styles

from questionary.constants import DEFAULT_QUESTION_PREFIX, DEFAULT_STYLE
from questionary.prompts.common import build_validator

WIN = sys.platform.startswith('win')


class Editor(object):
    def __init__(self,
                 editor=None,
                 env=None,
                 require_save=True,
                 extension='.txt'):
        self.editor = editor
        self.env = env
        self.require_save = require_save
        self.extension = extension

    def get_editor(self):
        if self.editor is not None and self.editor.lower() != "default":
            return self.editor

        for key in ['VISUAL', 'EDITOR']:
            rv = os.environ.get(key)
            if rv:
                return rv

        if WIN:
            return 'notepad'

        for editor in 'vim', 'nano':
            if os.system('which %s >/dev/null 2>&1' % editor) == 0:
                return editor

        return 'vi'

    def edit_file(self, filename):
        editor = self.get_editor()

        if self.env:
            environ = os.environ.copy()
            environ.update(self.env)
        else:
            environ = None

        try:
            c = subprocess.Popen('%s "%s"' % (editor, filename),
                                 env=environ, shell=True)
            exit_code = c.wait()
            if exit_code != 0:
                raise Exception('%s: Editing failed!' % editor)
        except OSError as e:
            raise Exception('%s: Editing failed: %s' % (editor, e))

    def edit(self, text):
        text = text or ''

        if text and not text.endswith('\n'):
            text += '\n'

        fd, name = tempfile.mkstemp(prefix='editor-', suffix=self.extension)
        try:
            if WIN:
                encoding = 'utf-8-sig'
                text = text.replace('\n', '\r\n')
            else:
                encoding = 'utf-8'
            text = text.encode(encoding)

            with io.open(fd, "wb") as f:
                f.write(text)

            timestamp = os.path.getmtime(name)

            self.edit_file(name)

            if self.require_save and os.path.getmtime(name) == timestamp:
                return None

            with io.open(name, 'rb') as f:
                rv = f.read()

            return rv.decode('utf-8-sig').replace('\r\n', '\n')
        finally:
            os.unlink(name)


def edit(text=None, editor=None, env=None, require_save=True,
         extension='.txt', filename=None):
    """Edits the given text in the defined editor.  If an editor is given
    (should be the full path to the executable but the regular operating
    system search path is used for finding the executable) it overrides
    the detected editor.  Optionally, some environment variables can be
    used.  If the editor is closed without changes, `None` is returned.  In
    case a file is edited directly the return value is always `None` and
    `require_save` and `extension` are ignored.

    If the editor cannot be opened a :exc:`UsageError` is raised.

    Note for Windows: to simplify cross-platform usage, the newlines are
    automatically converted from POSIX to Windows and vice versa.  As such,
    the message here will have ``\n`` as newline markers.

    :param text: the text to edit.
    :param editor: optionally the editor to use.  Defaults to automatic
                   detection.
    :param env: environment variables to forward to the editor.
    :param require_save: if this is true, then not saving in the editor
                         will make the return value become `None`.
    :param extension: the extension to tell the editor about.  This defaults
                      to `.txt` but changing this might change syntax
                      highlighting.
    :param filename: if provided it will edit this file instead of the
                     provided text contents.  It will not use a temporary
                     file as an indirection in that case.
    """

    editor = Editor(editor=editor, env=env, require_save=require_save,
                    extension=extension)
    if filename is None:
        return editor.edit(text)
    editor.edit_file(filename)


def question(message,
             qmark=DEFAULT_QUESTION_PREFIX,
             default=None,
             validate=None,
             style=None,
             eargs=None,
             **kwargs):
    eargs = eargs or {}
    merged_style = merge_styles([DEFAULT_STYLE, style])
    validator = build_validator(validate)

    for k, v in eargs.items():
        if not v.strip():
            raise ValueError(f"Value of arg '{k}' should not be empty.")

    editor = eargs.get("editor", None)
    ext = eargs.get("ext", ".txt")
    env = eargs.get("env", None)
    text = default
    filename = eargs.get("filename", None)
    multiline = (not editor)
    save = eargs.get("save", None)

    if editor:
        _text = edit(
            editor=editor,
            extension=ext,
            text=text,
            env=env,
            filename=filename,
            require_save=save
        )

        default = filename or _text

    def get_prompt_tokens():
        return [("class:qmark", qmark),
                ("class:question", f' {message} ')]

    p = PromptSession(get_prompt_tokens,
                      style=merged_style,
                      validator=validator,
                      multiline=True,
                      **kwargs)
    p.default_buffer.reset(Document(default))

    return p.app
