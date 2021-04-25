"""
Mission: Encapsulate, query & support an enumerated
verse-based, as well as a chapter-and-verse,
content-searching paradigm.

File: sierra_dao.py
Problem Domain: Database / DAO
Status: PRODUCTION / STABLE
Revision: 1.5

Note: A "sierra verse number" is a 1's based quote/verse
content-identification system. Sierra verse numbers can be
handy in cases where - like here - we crave a more succinct 
way of referring to those classic book:chapter:verse identifiers.
"""
import os
import os.path
import sys
import sqlite3


class SierraDAO:
    """Extract a nominal PROBLEM DOMAIN dictionary,
    from the database. Partial S3D2 pattern."""

    def __init__(self, cursor, bSaints=False):
        self.conn = cursor
        self.bSaints = bSaints
        self.sql_sel = "SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {zmatch}) ORDER BY V.ID;"

    def source(self):
        result = {
            "sierra": None,
            "book": None,
            "chapter": None,
            "verse": None,
            "text": None,
        }
        return dict(result)

    def random(self, bSaints=False):
        import random

        verse = 0
        if bSaints:
            verse = random.randrange(1, 37701)
        else:
            verse = random.randrange(1, 31103)
        return verse

    def get_sierra(self, vnum) -> dict():
        """ Lookup a single sierra verse number. """
        rows = self.search(f" V.ID={vnum} ")
        if rows:
            for row in list(rows):
                return row
        return self.source()

    def list_book_table(self):
        """Locate the book inventory.
        Return a complete row dictionary when found, else None."""
        cmd = "SELECT ID, Book, BookMeta, Token FROM SqlBooks ORDER BY ID;"
        res = self.conn.execute(cmd)
        try:
            zrow = res.fetchone()
            while zrow:
                result = dict()
                result["id"] = zrow[0]
                result["book"] = zrow[1]
                result["meta"] = zrow[2]
                result["title"] = result["book"].split(".")[2]
                result["token"] = zrow[3]
                yield result
                zrow = res.fetchone()
        except Exception as ex:
            print(ex, file=sys.stderr)
            raise ex
        return None

    def list_books(self) -> str():
        """Enumerate through each book in the database.
        Return the full name of the book, only.
        Return None if not found."""
        cmd = "SELECT Book FROM SqlBooks ORDER BY ID;"
        res = self.conn.execute(cmd)
        response = ""
        try:
            zrow = res.fetchone()
            while zrow:
                response = zrow[0]
                if zrow[0].find(".") != -1:
                    cols = zrow[0].split(".")
                    if self.bSaints == False and cols[1] != "nt" and cols[1] != "ot":
                        zrow = res.fetchone()
                        continue
                    response = cols[2]
                yield response
                zrow = res.fetchone()
        except Exception as ex:
            print(ex, file=sys.stderr)
            raise ex
        return None

    def search(self, where_clause):
        """ Search using a LIKE-match - one or many. """
        cmd = self.sql_sel.replace("{zmatch}", where_clause)
        res = self.conn.execute(cmd)
        response = self.source()
        try:
            zrow = res.fetchone()
            while zrow:
                response["sierra"] = str(zrow[4])
                response["book"] = zrow[1]
                if zrow[1].find(".") != -1:
                    cols = zrow[1].split(".")
                    if self.bSaints == False and cols[1] != "nt" and cols[1] != "ot":
                        zrow = res.fetchone()
                        continue
                    response["book"] = cols[2]
                response["chapter"] = zrow[2]
                response["verse"] = zrow[3]
                response["text"] = zrow[0]
                yield response
                zrow = res.fetchone()
        except Exception as ex:
            print(ex, file=sys.stderr)
            raise ex
        return None

    def get_sierra_book(self, book_name, chapt, verse):
        """Convert a BOOK NAME, chapter, and verse number
        into a 1's based "Sierra" verse number.
        Return None if none found."""
        bid = self.get_book_id(book_name)
        return self.get_sierra_num(bid, chapt, verse)

    def get_sierra_num(self, book_num, chapt, verse):
        """Convert a BOOK_ID, chapter, and verse number
        into a 1's based "Sierra" verse number.
        Return None if none found."""
        cmd = f"SELECT ID FROM SqlTblVerse WHERE (BookID = {book_num} AND \
        BookChapterID={chapt} AND BookVerseID={verse}) LIMIT 1;"
        try:
            res = self.conn.execute(cmd)
            if not res:
                return None
            zrow = res.fetchone()
            if zrow:
                return zrow[0]
        except:
            raise
        return None

    def get_book_title(self, book_name) -> str():
        """Return the full book-name for a short, or long, book name.
        Return None if the book_name is not in the database."""
        dao = SierraDAO.GetDAO(True)
        if not dao:
            return None
        zup = book_name.strip().upper()
        for book in dao.list_book_table():
            if zup == book["title"].strip().upper():
                return book["title"]
            if zup == book["token"].strip().upper():
                return book["title"]
        return None

    def get_book_id(self, book_name):
        """Return the database ID from EITHER a book token, or name.
        Return None if not found / error."""
        if len(book_name) < 5:
            book_name = self.get_book_title(book_name)
            if not book_name:
                return None
        cmd = f"SELECT ID FROM SqlBooks WHERE Book LIKE '%{book_name}%' LIMIT 1;"
        try:
            res = self.conn.execute(cmd)
            zrow = res.fetchone()
            if zrow:
                return zrow[0]
        except:
            raise
        return None

    def get_from_place(self, vnum):
        cmd = f"SELECT ID, Verse FROM sqltblverse Where ID>={vnum} ORDER BY Id LIMIT 10;"
        try:
            res = self.conn.execute(cmd)
            zrow = res.fetchall()
            if zrow:
                yield zrow
        except:
            raise
        return None

    '''def set_bookmark(self, vnum):
        

    def get_bookmark(self):
        """Return all bookmarked verses"""
        cmd = f"SELECT ID FROM SqlTblVerse WHERE VerseType=1;"
        try:
            res = self.conn.execute(cmd)
            zrow = res.fetchall()
            if zrow:
                return zrow
        except:
            raise
        return None
'''

    @staticmethod
    def GetBookId(book_name):
        """Return the database ID from EITHER a book token, or name.
        Return None if not found / error."""
        dao = SierraDAO.GetDAO(True)
        return dao.get_book_id(book_name)

    @staticmethod
    def ParseClassicVerse(cvn):
        """Is the CLASSIC reference valid? (string plus two numbers.)
        Return dictionary if found, else False."""
        cols = cvn.split(":")
        if len(cols) is 3:
            try:
                chapt = int(cols[1])
                if chapt < 1:
                    return False
                verse = int(cols[2])
                if verse < 1:
                    return False
                book = SierraDAO.GetBookId(cols[0])
                if book:
                    return {"book": book, "chapter": chapt, "verse": verse}
            except Exception as ex:
                print(ex)
        return False
    
    @staticmethod
    def Connect(bSaints=False):
        """ Connect to the database & return same """
        db = "biblia02.sqlt3"
        if os.path.exists("./" + db):
            db = "./" + db
        else:
            db = "./PyKJV/" + db
        if not os.path.exists(db):
            print("Error: Unable to locate database")
            quit()
        conn = sqlite3.connect(db)
        # conn.row_factory = dict_factory
        return conn

    @staticmethod
    def GetDAO(bSaints=False):
        conn = SierraDAO.Connect(bSaints)
        curs = conn.cursor()
        dao = SierraDAO(curs, bSaints)
        return dao

    @staticmethod
    def ListBooks(bSaints=False) -> str():
        """ Get the major book names """
        dao = SierraDAO.GetDAO(bSaints)
        if not dao:
            return None
        books = dao.list_books()
        for book in books:
            yield book

    @staticmethod
    def ListBookTags(bSaints=False) -> str():
        """ Get the major book tokens """
        for name in SierraDAO.ListBooks():
            yield name.replace(" ", "")[0:4]
