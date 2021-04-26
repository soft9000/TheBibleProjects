import abc


class AbsPage(abc.ABC):
    ''' 
    An opportunity to manage a pagenated view 
    into a larger collection of items 
    '''
    def __init__(self, max_lines, page_size = 10, line_num = 1):
        self.max_lines = max_lines
        self._page_size = page_size
        self._line_num = line_num
    
    @property
    def page_size(self):
        ''' Read the view / page size '''
        return self._page_size
    
    @page_size.setter
    def page_size(self, page_size):
        ''' Set the view / page size '''
        self._page_size = page_size
    
    @property
    def line_num(self):
        ''' Read the page-top '''
        return self._line_num
    
    @line_num.setter
    def line_num(self, line_num):
        ''' Set the page top '''
        self._line_num = line_num
        self._normalize()

    def page_inc(self):
        self._line_num += self._page_size
        self._normalize()

    def page_dec(self):
        self._line_num -= self._page_size
        self._normalize()

    def line_inc(self):
        self._line_num += 1
        self._normalize()

    def line_dec(self):
        self._line_num -= 1
        self._normalize()

    def set_line(self, line_num):
        self._line_num = line_num
        self._normalize()
    
    def first_page(self) -> int:
        return 1
    
    def last_page(self) -> int:
        return self.max_lines - self._page_size + 1
    
    def _normalize(self):
        if self._line_num > self.max_lines:
            self._line_num = self.last_page()
        if self._line_num < self.first_page():
            self._line_num = self.first_page()
        delta = self._line_num + self._page_size
        if delta > self.max_lines:
            self._line_num = self.last_page()

    @abc.abstractmethod
    def get_page(self) -> list:
        ''' Get the present list / item view '''
        pass
