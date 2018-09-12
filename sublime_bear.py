from urllib.parse import quote
import webbrowser

import sublime
import sublime_plugin


class BearApi(object):

    BASE_URL = 'bear://x-callback-url/{action}'

    def xcall(self, action, parameters):
        url = self.BASE_URL.format(action=action)

        if parameters:
            parameters = '&'.join(
                '%s=%s' % (self._quote(k), self._quote(v))
                for k, v in parameters.items()
            )
            url = '%s?%s' % (url, parameters)

        self._open_url(url)

    def _quote(self, s):
        if isinstance(s, bool):
            s = 'yes' if s else 'no'
        else:
            s = str(s)

        return quote(s)

    def _open_url(self, url):
        webbrowser.open(url)


class BearNote(object):

    def __init__(self):
        self.api = BearApi()

    def create(self, text):
        self.api.xcall('create', dict(text=text))


class BearCreateNoteCommand(sublime_plugin.TextCommand):
    """Sublime Text command to create note in Bear from selected text."""

    def is_text_selected(self):
        selections = self.view.sel()
        if all(s.empty() for s in selections):
            return False

        return True

    def run(self, edit):
        selections = self.view.sel()

        if self.is_text_selected():
            note_text = '\n'.join(self.view.substr(sel) for sel in selections)
        else:
            note_text = self.view.substr(sublime.Region(0, self.view.size()))

        BearNote().create(note_text)
