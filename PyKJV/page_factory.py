import abs_page

class page_test(abs_page.AbsPage):

    def __init__(self, max_lines, page_size = 10):
        super().__init__(max_lines, page_size)

    def get_page(self) -> list:
        if self._line_num > 0:
            nelem = self._line_num + self._page_size
            return list(range(self._line_num, nelem))
        return list()

if __name__ == '__main__':
    from menu import do_menu
    pager = page_test(30, 5)

    def do_display():
        for line in pager.get_page():
            print('@', line)

    def do_lineadv():
        pager.line_dec()
        do_display()

    def do_pageadv():
        pager.page_dec()
        do_display()

    def do_linedec():
        pager.line_inc()
        do_display()

    def do_pagedec():
        pager.page_inc()
        do_display()

    def do_goto():
        which = input("Go to: ")
        if which.isnumeric():
            pager.set_line(int(which))
            do_display()
        else:
            print("meh...")

    options = [
        ("a", "lnup", do_linedec),
        ("z", "pgup", do_pagedec),
        ("s", "lndn", do_lineadv),
        ("x", "pgdn", do_pageadv),
        ("g", "goto", do_goto),
        ("q", "Quit Program", quit),
    ]
    do_display()
    do_menu("Main Menu", "Option = ", options, "#")
    print('.')

