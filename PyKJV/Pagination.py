import sqlite3
from sierra_dao import SierraDAO
from verse import Verse
import abs_page
from menu import do_menu

class Page():

    # cursor is the result of an sql statement
    def __init__(self, statement):
        self.statement = statement
        self.cmd = "SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND BookChapterID={BookID} AND BookVerseID<={VerseID}) LIMIT 10;"
        #i could make cmd not have a "where" statement and add where clauses as needed

    def retrieve_title(self, ID):
        cmd = f"select Book from SqlBooks where ID = {ID};"
        Dao = SierraDAO.GetDAO()
        Book_Title = Dao.conn.execute(cmd)
        for Line1 in Book_Title:
            for Line2 in Line1:
                Book_Title = Line2.split(".")
                Book_Title = Book_Title[2]
        return Book_Title

    def convert_sql_int(self, RSQL):
        # Takes a raw SQL Result and converts the first line given into an integer
        for line1 in RSQL:
            for line in line1:
                return int(line)
    
    def count_chapter_verses(self, book_ID, Chapter_ID):      
        book_ID = SierraDAO.GetBookId(book_ID)
        cmd = "select COUNT(BookVerseID) from SqlTblVerse where (BookID = {Z_ID} AND BookChapterID={BookID});"
        cmd = cmd.format(Z_ID=book_ID, BookID=Chapter_ID)
        DAO = SierraDAO.GetDAO()
        Count_Pages = DAO.conn.execute(cmd)
        Total_Pages = self.convert_sql_int(Count_Pages)
        return Total_Pages

    def count_books_chapters(self, book_ID):
        book_ID = SierraDAO.GetBookId(book_ID)
        cmd = "select MAX(BookChapterID) from SqlTblVerse where BookID = {Z_ID};"
        cmd = cmd.format(Z_ID=book_ID)
        DAO = SierraDAO.GetDAO()
        Count_Pages = DAO.conn.execute(cmd)
        Total_Pages = self.convert_sql_int(Count_Pages)
        return Total_Pages

    def page_up(self):
        if len(self.statement) == 3:
            Z_ID = SierraDAO.GetBookId(self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND \
            BookChapterID={self.statement[1]} AND BookVerseID>={self.statement[2]}) LIMIT 10;"
            N_page = dao.conn.execute(cmd)

        elif len(self.statement) == 1:
            Z_ID = SierraDAO.GetBookId(self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
            FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {self.statement[0]}) ORDER BY V.ID;"
            N_page = dao.conn.execute(cmd)
        verse = N_page.fetchall()
        return verse

    def page_down(self):
        if len(self.statement) == 3:
            Z_ID = SierraDAO.GetBookId(self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND \
            BookChapterID={self.statement[1]} AND BookVerseID<={self.statement[2]}) LIMIT 10;"
            N_page = dao.conn.execute(cmd)

        elif len(self.statement) == 1:
            Z_ID = SierraDAO.GetBookId(self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
            FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {self.statement[0]}) ORDER BY V.ID;"
            N_page = dao.conn.execute(cmd)
        verse = N_page.fetchall()
        return verse

    def show_error(self):
        pass

    def end_of_path(self):
        pass


class PageOps(abs_page.AbsPage):
    ''' Here is a way to use the main parser '''
    
    def __init__(self, statement,Page_Size = 10):
        # i need to replace statement with the book,chapter,verse equivilent
        #it is very possible that the "do" methods will become artifacts
        self.statement = statement

        self.book = statement[0]
        self.chapter = statement[1]

        self.Select = "select {} "
        self.From = " From {} "
        self.Where = "Where "

        #when you receive a statement. then find out how many verses it has in total
        self.Max_Size = Page(statement).count_chapter_verses(statement[0],statement[1])
        #used for returning paginations "determined by the user"
        super().__init__(self.Max_Size,Page_Size,statement[2])

    def do_next_page(self):
        display = Verse()
        self.statement[2] = int(self.statement[2]) + 10 
        zpage = Page(self.statement)
        verse = zpage.page_up()

        # if you did not receive a verse....
        if len(verse) == 0:

            # construct a count self.statement to retrieve the total number of verses
            # see about replacing these with properties
            Total_Pages = zpage.count_chapter_verses(
                self.statement[0], self.statement[1])
            Total_Chapters = zpage.count_books_chapters(self.statement[0])

            # if your trying to get a chapter that is not within the book. then switch to the next book
            if int(self.statement[1]) >= Total_Chapters:

                BookTitle = SierraDAO.GetBookId(self.statement[0]) + 1
                BookTitle = zpage.retrieve_title(BookTitle)

                self.statement[0] = BookTitle
                self.statement[1] = 1
                self.statement[2] = 0

                verse = Page(self.statement)
                verse = verse.page_up()
            # if the verse we are currently at is equal to or greater than 
            # the page count "number of verses in our book" then turn the chapter
            elif self.statement[2] >= Total_Pages:

                self.statement[1] = int(self.statement[1]) + 1
                self.statement[2] = 0
                verse = Page(self.statement)
                verse = verse.page_up()

        for n in verse:
            zformat = display.wrap(n[0])
            display.show(zformat)

    def do_last_page(self):
        display = Verse()
        self.statement[2] = int(self.statement[2]) - 10 
        zpage = Page(self.statement)
        verse = zpage.page_down()

        # if you did not receive a verse....
        if len(verse) == 0:
            # construct a count self.statement to retrieve the total number of verses
            Total_Pages = zpage.count_chapter_verses(
                self.statement[0], self.statement[1])
            Total_Chapters = zpage.count_books_chapters(self.statement[0])

            # if your trying to get a chapter that is not within the book, then 
            # switch to the next book
            if int(self.statement[1]) >= Total_Chapters:
                BookTitle = SierraDAO.GetBookId(self.statement[0]) - 1
                BookTitle = zpage.retrieve_title(BookTitle)

                self.statement[0] = BookTitle
                self.statement[1] = 1
                self.statement[2] = 0

                verse = Page(self.statement)
                verse = verse.page_down()
            # if the verse we are currently at is equal to or greater than the 
            # page count "number of verses in our book" then turn the chapter
            elif self.statement[2] >= Total_Pages:
                self.statement[1] = int(self.statement[1]) - 1
                self.statement[2] = 0
                verse = Page(self.statement)
                verse = verse.page_up()
    def Next_Chapter(self):
        """resets the chapter and verse value "represent the beggining of the next chapter in a book" """
        self.chapter = self.chapter + 1
        self.line_num(1)

    def EndOfPage(self):
        """if your verse is greater than the maximum pages in a chapter then go to the next chapter"""
        if self.verse > self.Max_Size:
            Next_Chapter()

     # should this be sent to the sierra_dao object?
    def constr_where(self, *args):
        cmd = self.Where
        
        for items in args:
            cmd +=(f'{items} ')
            if args.index(items) < len(args) - 1:
                cmd += 'AND '

        return cmd

    def get_page(self) -> list:
        '''returns a list of verses based on a given list'''
        if self._line_num < 0:
            return list()

        Statement = self.statement
        DAO = SierraDAO.GetDAO()
        Book_ID = DAO.get_book_id(self.book)
        # this is a legitimate pagination statement
        #cmd = 'SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND BookChapterID={ChapterID}) ORDER BY bookID LIMIT 10 OFFSET {VerseID};'
        cmd = self.Select.format("Verse")
        cmd += self.From.format("SqlTblVerse")
        cmd += self.constr_where(f'BookID = {Book_ID}',f'BookChapterID= {self.chapter}')
        cmd += f'ORDER BY bookID LIMIT 10 OFFSET {self._line_num - 1};'
        
        #cmd = cmd.format(Z_ID=Book_ID,ChapterID=self.chapter,VerseID=self._line_num - 1)

        verses = DAO.conn.execute(cmd)
        all_verse = verses.fetchmany(10)
        return all_verse

    def do_display(self):
        for line in self.get_page():
            for line2 in line:
                print('@', line2)

    def do_lineadv(self):
        
        self.line_inc()
        self.do_display()
        

    def do_pageadv(self):
        self.page_inc()
        self.do_display()
        

    def do_linedec(self):
        
        self.line_dec()
        self.do_display()
        
        

    def do_pagedec(self):
        self.page_dec()
        
        self.do_display()
        

    def do_goto(self):
        which = input("Go to: ")
        if which.isnumeric():
            self.set_line(int(which))
            self.do_display()
        else:
            print("meh...")


    def display_options(self):
        options = [
        ("a", "lnup", self.do_lineadv),
        ("z", "pgup", self.do_pageadv),
        ("s", "lndn", self.do_linedec),
        ("x", "pgdn", self.do_pagedec),
        ("g", "goto", self.do_goto),
        ("q", "Quit Program", quit),
    ]
        self.do_display()
        do_menu("Main Menu", "Option = ", options, "#")
        self.EndOfPage()