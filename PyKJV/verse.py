import textwrap

class Verse:

    def __init__(self, width=25, margin=5, initial_indent=' '):
        self._wrap = textwrap.TextWrapper()
        self._wrap.width = width
        self._margin = margin
        self._wrap.initial_indent = initial_indent
        self._line_size = self._wrap.width + self._margin
        self._mask = ' | {:<' + str(self._line_size) + '} |'
    
    def center(self, line, char = ' '):
        if len(line) > self._line_size:
            line = line[0:self._line_size]
        return self._mask.format(line.center(self._line_size, char))
    
    def wrap(self, line) -> list():
        results = list()
        for w in self._wrap.wrap(line):
            rline = self._mask.format(w)
            results.append(rline)
        results.append("\n")
        return results