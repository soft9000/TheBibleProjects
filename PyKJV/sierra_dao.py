'''
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
'''
import os
import os.path
import sys
import sqlite3


class SierraDAO:
    ''' Extract a nominal PROBLEM DOMAIN dictionary,
        from the database. Partial S3D2 pattern.'''
    
    def __init__(self, cursor, bSaints=False):
        self.conn = cursor
        self.bSaints = bSaints
        self.sql_sel = "SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID AND {zmatch}) ORDER BY V.ID;"

    def source(self):
        result = {
            "sierra":None,
            "book":None,
            "chapter":None,
            "verse":None,
            "text":None,
           }
        return dict(result)

   
    def random(self, bSaints = False):
        import random
        verse = 0
        if bSaints:
            verse = random.randrange(1, 37701)
        else:
            verse = random.randrange(1, 31103)
        return verse


    def classic2sierra(self, book, chapt, verse):
        # print([book, chapt, verse], file=sys.stderr)
        cmd = f"SELECT V.ID FROM SqlTblVerse AS V JOIN SqlBooks as B \
WHERE (B.ID=BookID) AND BOOK LIKE '%{book}%' AND BookChapterID='{chapt}' AND BookVerseID='{verse}' LIMIT 1;"
        print(cmd, file=sys.stderr)
        res = self.conn.execute(cmd)
        try:
            zrow = res.fetchone()
            print(zrow, file=sys.stderr)
            if zrow:
                return zrow[0]
        except:
            raise
        return None
            
    def search_verse(self, sierra_num) -> dict():
        ''' Lookup a single sierra verse number. Presently unloved. '''
        rows = self.search(f" V.ID={sierra_num} ")
        if not rows:
            return self.source()
        for row in rows:
            return row

    def list_books(self) -> str():
        ''' Locate the book inventory - Name of book, only '''
        cmd = "SELECT Book FROM SqlBooks ORDER BY ID;"
        res = self.conn.execute(cmd)
        response = ''
        try:
            zrow = res.fetchone()
            while zrow:
                response = zrow[0]
                if zrow[0].find('.') != -1:
                    cols = zrow[0].split('.')
                    if self.bSaints == False and cols[1] != 'nt' and cols[1] != 'ot':
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
        ''' Search using a LIKE-match - one or many. '''
        cmd = self.sql_sel.replace('{zmatch}', where_clause)
        res = self.conn.execute(cmd)
        response = self.source()
        try:
            zrow = res.fetchone()
            while zrow:
                response['sierra'] = str(zrow[4])
                response['book'] = zrow[1]
                if zrow[1].find('.') != -1:
                    cols = zrow[1].split('.')
                    if self.bSaints == False and cols[1] != 'nt' and cols[1] != 'ot':
                        zrow = res.fetchone()
                        continue
                    response['book'] = cols[2]
                response['chapter'] = zrow[2]
                response['verse'] = zrow[3]
                response['text'] = zrow[0]
                yield response
                zrow = res.fetchone()
        except Exception as ex:
            print(ex, file=sys.stderr)
            raise ex
        return None

    
    @staticmethod
    def GetDAO(bSaints=False):
        ''' Connect to the database & return the DAO '''
        db = "biblia.sqlt3"
        if os.path.exists("./" + db):
            db = "./" + db
        else:
            db = "./PyKJV/" + db
        if not os.path.exists(db):
            print("Error: Unable to locate database")
            quit()
        conn = sqlite3.connect(db)
        # conn.row_factory = dict_factory
        curs = conn.cursor()
        dao = SierraDAO(curs, bSaints)
        return dao

    
    @staticmethod
    def ListBooks(bSaints=False) -> str():
        ''' Get the major book names '''
        dao = SierraDAO.GetDAO(bSaints)
        if not dao:
            return None
        books = dao.list_books()
        for book in books:
            yield book
    
    @staticmethod
    def ListBookTags(bSaints=False) -> str():
        ''' Get the major book tokens '''
        for name in SierraDAO.ListBooks():
            yield name.replace(' ', '')[0:4]

if __name__ == "__main__":
    ''' Ye Olde Testing '''
    from verse import Verse
    for ss, row in enumerate(SierraDAO.ListBooks(True), 1):
        print(ss, row)
    for ss, row in enumerate(SierraDAO.ListBooks(True), 1):
        print(ss * 1000, row)
    dao = SierraDAO.GetDAO()
    v = Verse()
    for row in dao.search("verse LIKE '%PERFECT%'"):
        line = row['text']
        print(v.center(' {0} {1}:{2} '.format(row['book'],row['chapter'],row['verse']), '='))
        for row in v.wrap(line):
            print(row)
