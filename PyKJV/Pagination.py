import sqlite3
from sierra_dao import SierraDAO
from verse import Verse


class Page:

    # cursor is the result of an sql self.statement
    def __init__(self, statement):
        self.self.statement = self.statement
        self.cmd = "SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND BookChapterID={BookID} AND BookVerseID<={VerseID}) LIMIT 10;"

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
        if len(self.self.statement) == 3:
            Z_ID = SierraDAO.GetBookId(self.self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND \
            BookChapterID={self.self.statement[1]} AND BookVerseID>={self.self.statement[2]}) LIMIT 10;"
            N_page = dao.conn.execute(cmd)

        elif len(self.self.statement) == 1:
            Z_ID = SierraDAO.GetBookId(self.self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
            FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {self.self.statement[0]}) ORDER BY V.ID;"
            N_page = dao.conn.execute(cmd)
        verse = N_page.fetchall()
        return verse

    def page_down(self):
        if len(self.self.statement) == 3:
            Z_ID = SierraDAO.GetBookId(self.self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND \
            BookChapterID={self.self.statement[1]} AND BookVerseID<={self.self.statement[2]}) LIMIT 10;"
            N_page = dao.conn.execute(cmd)

        elif len(self.self.statement) == 1:
            Z_ID = SierraDAO.GetBookId(self.self.statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
            FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {self.self.statement[0]}) ORDER BY V.ID;"
            N_page = dao.conn.execute(cmd)
        verse = N_page.fetchall()
        return verse

    def show_error(self):
        pass

    def end_of_path(self):
        pass


class PageOps():
    ''' Here is a way to use the main parser '''

    def __init__(self, statement):
        self.statement = statement

    def do_next_page(self):
        self.self.statement[2] = int(self.self.statement[2]) + 10 # TODO: this is broken - please fix
        zpage = Page(self.self.statement)
        verse = zpage.page_up()

        # if you did not receive a verse....
        if len(verse) == 0:

            # construct a count self.statement to retrieve the total number of verses
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
        self.statement[2] = int(self.self.statement[2]) + 10 # TODO: this is broken - please fix
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
                verse = verse.down()
            # if the verse we are currently at is equal to or greater than the 
            # page count "number of verses in our book" then turn the chapter
            elif self.statement[2] >= Total_Pages:
                self.statement[1] = int(self.statement[1]) - 1
                self.statement[2] = 0
                verse = Page(self.statement)
                verse = verse.page_up()


