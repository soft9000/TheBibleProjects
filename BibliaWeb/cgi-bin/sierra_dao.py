import sys


class SierraDAO:
    ''' Extract a nominal PROBLEM DOMAIN dictionary,
        from the database. Partial S3D2 pattern.'''
    
    def __init__(self, cursor, bSaints=False):
        self.conn = cursor
        self.bSaints = bSaints
        self.sql_sel = "SELECT Verse, Book, BookChapterID, BookVerseID, V.ID, BookID \
FROM SqlTblVerse AS V JOIN SqlBooks as B WHERE (B.ID=BookID) AND {zmatch} ORDER BY V.ID;"

    def source(self):
        result = {
            "sierra":None,
            "book":None,
            "chapter":None,
            "verse":None,
            "text":None,
           }
        return result
            
    def search_verse(self, sierra_num):
        ''' Lookup a single sierra verse number. Presently unloved. '''
        for result in self.search(f"V.ID={sierra_num} LIMIT 1"):
            yield result

    def search_books(self):
        ''' Locate the book inventory - Name of book, only '''
        cmd = "SELECT Book FROM SqlBooks ORDER BY ID;"
        res = self.conn.execute(cmd)
        response = self.source()
        try:
            zrow = res.fetchone()
            while zrow:
                response['book'] = zrow[0]
                if zrow[0].find('.') != -1:
                    cols = zrow[0].split('.')
                    if self.bSaints == False and cols[1] != 'nt' and cols[1] != 'ot':
                        zrow = res.fetchone()
                        continue
                    response['book'] = cols[2]
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

    def get_book_title(self, book_name):
        dao = SierraDAO.GetDAO(True)
        if not dao:
            return None
        for book in dao.list_books():
            pass

    def get_book_id(self, book_name):
        if isinstance(book_name, int()):
            return book_name
        if len(book_name) > 5:
            book_name = get_book_title(book_name)
        cmd = f"SELECT ID FROM SqlBooks WHERE LIMIT 1;"
        print(cmd, file=sys.stderr)
        try:
            res = self.conn.execute(cmd)
            zrow = res.fetchone()
            print(zrow, file=sys.stderr)
            if zrow:
                return zrow[0]
        except:
            raise
        return None

    @staticmethod
    def GetBookId(book_name):
        ''' Return the ID for either a Name or a Token '''
        cmd = "SELECT ID FROM SqlBooks WHERE "
        if len(book_name) > 4:
            cmd += f'TOKEN = "{book_name}"'
        else:
            cmd += f'Book = "{book_name}"'
        cmd += " LIMIT 1;"
        dao = SierraDAO.GetDAO(True)

    @staticmethod
    def IsValidVerse(cvn):
        ''' Its the reference valid? (string plus two integers) '''
        cols = cvn.split(':')
        if len(cols) is 3:
            try:
                chapt = int(cols[1])
                verse = int(cols[2])
                book  = GetBookId(cols[0])
                return True
            except:
                pass
        return False        

