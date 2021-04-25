"""
Mission: Word-wrap a long line into a "hereis" worthy,
console-printable, block 'o text.

File: verse.py
Rev: 0.1
"""
import textwrap
from sierra_dao import SierraDAO


class Verse:
    def __init__(self, width=25, margin=5, initial_indent=" "):
        self._wrap = textwrap.TextWrapper()
        self._wrap.width = width
        self._margin = margin
        self._wrap.initial_indent = initial_indent
        self._line_size = self._wrap.width + self._margin
        self._mask = " | {:<" + str(self._line_size) + "} |"

    def get_verse(self, verse) -> str():
        dao = SierraDAO.GetDAO()
        verse = dao.get_sierra(verse)
        view = Verse()
        if not verse:
            return view.wrap(None)
        return view.wrap(verse["text"].strip())

    def random(self, bSaints=False) -> list():
        verse = SierraDAO.random(bSaints)
        lines = self.get_verse(verse)
        return lines

    def center(self, line, char=" "):
        if len(line) > self._line_size:
            line = line[0: self._line_size]
        return self._mask.format(line.center(self._line_size, char))

    def wrap(self, line) -> list():
        if not line:
            line = "(none)"
        if isinstance(line, list):
            results = list()
            replaceable = "()'[]"
            for w in self._wrap.wrap(str(line)):
                for r in replaceable:
                    w = w.replace(r,"")
                    w = w.replace(", ~~~~~~~~~~~~~~~~~~~~~~,","\n |")
                    w = w.replace("~~~~~~~~~~~~~~~~~~~~~~,","\n |")
                rline = self._mask.format(w)
                results.append(rline)
            return results
        else:
            results = list()
            for w in self._wrap.wrap(line):
                rline = self._mask.format(w)
                results.append(rline)
            results.append("\n")
        return results

    def list_books(self) -> list():
        """ Create a verse-formatted list of book TAGS """
        cols = 5
        cntr = int(self._wrap.width / cols) + 1
        results = list()
        line = ""
        for ss, book in enumerate(SierraDAO.ListBookTags()):
            if ss % cols == 0:
                results.append(line.center(self._line_size))
                line = book.center(cntr)
            else:
                line += book.center(cntr)
        if len(line) > 0:
            results.append(line.center(self._line_size))
        return results

    def show(self, lines):
        """ Display the result of a verse value """
        if not lines:
            print(self.wrap(None))
            return
        for line in lines:
            print(line)
