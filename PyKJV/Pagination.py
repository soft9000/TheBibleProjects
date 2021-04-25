import sqlite3
from sierra_dao import SierraDAO
from verse import Verse


class Page:

    # cursor is the result of an sql statement
    def __init__(self, Statement):
        self.Statement = Statement
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
        if len(self.Statement) == 3:
            Z_ID = SierraDAO.GetBookId(self.Statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND \
            BookChapterID={self.Statement[1]} AND BookVerseID>={self.Statement[2]}) LIMIT 10;"
            N_page = dao.conn.execute(cmd)

        elif len(self.Statement) == 1:
            Z_ID = SierraDAO.GetBookId(self.Statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
            FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {self.Statement[0]}) ORDER BY V.ID;"
            N_page = dao.conn.execute(cmd)
        verse = N_page.fetchall()
        return verse

    def page_down(self):
        if len(self.Statement) == 3:
            Z_ID = SierraDAO.GetBookId(self.Statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse FROM SqlTblVerse WHERE (BookID = {Z_ID} AND \
            BookChapterID={self.Statement[1]} AND BookVerseID<={self.Statement[2]}) LIMIT 10;"
            N_page = dao.conn.execute(cmd)

        elif len(self.Statement) == 1:
            Z_ID = SierraDAO.GetBookId(self.Statement[0])
            dao = SierraDAO.GetDAO()
            cmd = f"SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
            FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {self.Statement[0]}) ORDER BY V.ID;"
            N_page = dao.conn.execute(cmd)
        verse = N_page.fetchall()
        return verse

    def show_error(self):
        pass

    def end_of_path(self):
        pass
