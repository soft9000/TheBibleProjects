#!/usr/bin/python3
print("Content-Type:text/html; charset=UTF-8\n")
print("<!DOCTYPE html>")

import cgi
import sys
import cgitb
import sqlite3

from ajaxers    import *
from sierra_dao import SierraDAO as SierraDAO

# Include "Another Testament":
bSaints = True


class FormLookup:
    ''' Locate a verse EITHER by Sierra @ number, or
        by the classic book, chapter, & verse. '''

    def __init__(self):
        pass
    
    def can_exec(self, cgi_data):
        if 'xlookup2' in cgi_data:
            return True
        return False

    def exe_cgi_form(self, data, curs):
        cols = data['xlookup2'].split('|')
        sierra = cols[0]
        if len(sierra):
            if sierra[0] == '@':
                sierra = sierra[1:]
            try:
                sierra = int(sierra)
                if sierra:
                    return DoAjaxRecall(curs, str(sierra))
            except:
                pass
        global bSaints
        dao = SierraDAO(curs, bSaints)
        cv = cols[1].split(':')
        print(cv, file=sys.stderr)
        if len(cv) == 2:
            try:
                chapt = int(cv[0]); verse = int(cv[1])
                if chapt and verse:
                    sierra = dao.classic2sierra(cols[2], str(chapt), str(verse))
                    if sierra:
                        return DoAjaxRecall(curs, str(sierra))
            except:
                raise
        return "Unknown verse. Try again?"

    def get_html(self, cursor, bSaints=False):
        result = '<div>Use Classic, or @Number:'
        result += "<div class='eor'>"
        result += "<p><i>'Sierra Verse' Number:</i></p>"
        result += "<p>@Number<input type='text' id='id_sierra' class='numin' value='@0000'></p>"
        result += "<br>"
        result += "</div>"
        result += "<div class='eor'>"
        result += "<p><i>'Classic Verse' Number:</i></p>"
        dao = SierraDAO(cursor, bSaints)
        result += "<p><select id='id_book'><option></option><br>"
        for verse in dao.search_books():
            result += f"<option>{verse['book']}</option><br>"
        result += "</select>"
        result += "<input type='text' id='id_verse' class='numin' value='0:00'></p>"
        result += "<br>"
        result += "</div>"
        result += '<input type="button" value="Lookup" onclick="AxLookup()">'
        result += "<br><br>"
        result += "</div>"
        return result


class FormMenu:
    def can_exec(self, cgi_data):
        bWant = 'xmenu' in cgi_data
        return bWant
    
    def exe_cgi_form(self, cgi_data, curs):
        global bSaints
        ''' React to menu-button click '''
        mOpt = cgi_data['xmenu']
        result = ""
        if mOpt == "xsearch":
            global formSearch
            result += formSearch.get_html() # GLOBAL
        elif mOpt == "xlibrary":
            result += FrmBooks(curs, '')    # GLOBAL
        elif mOpt == "xlookup":
            result += formLookup.get_html(curs, bSaints) # GLOBAL
        elif mOpt == "xcopy_bookmarks":
            result += f"<p><b>AxMenu:<b> {mOpt} ACK!</p>"
        elif mOpt == "xpaste_bookmarks":
            result += f"<p><b>AxMenu:<b> {mOpt} ACK!</p>"
        else:
            result = f"Error: [{mOpt}] Undefined..."
        return result
    
    def get_html(self):
        ''' Create menu-buttons '''
        
        style = 'zmenu'
        result = f"<div class='{style}'>\n"
        btns = {
            "Lookup":"sierra.py?xmenu=xlookup",
            "Search":"sierra.py?xmenu=xsearch",
            "Library":"sierra.py?xmenu=xlibrary",
            # "Copy Bookmarks":"sierra.py?xmenu=copy_bookmarks",
            # "Paste Bookmarks":"sierra.py?xmenu=paste_bookmarks",
            }
        result = ''
        for name in btns:
            ztag = 'x' + name.lower().replace(' ', '_')
            result += f"<label class='zbtn' onclick='AxMenu(\"{ztag}\")'>{name}</label>"
        result += "</div>"
        return result


class FormSearch:

    def __init__(self, root_name='Search'):
        self.root_name = root_name
        self.value = ''
        self.html_form = '''
<div class='eor'>
<p><i>Look for:</i></p>
    <input type="text" id="search_words" name="search_words" value="{self.value}">  
    <input type="button" value="Search" onclick="AxVal('?search_words=', 'search_words','zbooks')">  
<br><br>
</div>
'''

    def get_html(self):
        response = "Comma (,) Separated:<br>"
        response += str(self.html_form).replace('{self.value}', '')
        return response

    def can_exec(self, cgi_data):
        bWant = 'search_words' in cgi_data
        return bWant

    @staticmethod
    def MakeLike(zfield, zwords):
        result = ''
        for word in zwords:
            if not result:
                result = f"{zfield} LIKE "
            else:
                result += f" AND {zfield} LIKE "
            result += f"'%{word}%'"
        return result
    
    def exe_cgi_form(self, cgi_data, conn):
        searched = cgi_data['search_words']
        words = searched.split(',')
        zmatch = FormSearch.MakeLike('Verse', words)
        response = ""
        response +=  str(self.html_form).replace('{self.value}', searched)
        cmd = f"SELECT COUNT(*) FROM SqlTblVerse WHERE {zmatch};"
        res = conn.execute(cmd)
        zhits = str(res.fetchone()[0])
        response += f'<br><label class="message"><br>Matched {zhits} verses:</label><br>'
        global bSaints
        db = SierraDAO(conn, bSaints)
        zrows = db.search(zmatch)
        for ss, zrow in enumerate(zrows, 1):
            response += f"<hr><label onclick='AxVerse(\"{zrow['sierra']}\")'>"
            response += f"<br>{ss}: {zrow['book']}</i> <b>{zrow['chapter']}:{zrow['verse']}</b>"
            verse = zrow['text']
            for word in words:
                verse = verse.replace(word, f"<b>{word}</b>")
            response += f"<br>{verse} ...</label>"
        return response

    
def LinkBook(book):
    return f"<label class='xlink' onclick='AxBook(\"{book}\")'>{book}</label>"


def LinkVerse(pkVerse):
    return f"<label class='xlink' onclick='AxBookmark({pkVerse}, \"xbkmrk\")'>{pkVerse}</label>"


def getBookName(curs, pk):
    res = curs.execute(f"SELECT BOOK from SqlBooks WHERE ID ={pk} LIMIT 1;")
    try:
        zrow = res.fetchone()
        if zrow:
            return zrow[0].split('.')[2]
    except Exception as ex:
        print(ex)
        return None


def FrmBooks(curs, style):
    ''' The main book siaplay - no Ajax. '''
    global bSaints
    res = curs.execute("SELECT BOOK FROM SqlBooks;")
    result = f"<div class='{style}' id='zbooks'>\n"
    result += "<ul>\n"
    prev = None
    for book in res.fetchall():
        cols = book[0].split(".")
        zname = cols[2]
        if cols[1] == 'ot':
            zset = 'Old Testament'
        elif cols[1] == 'nt':
            zset = 'New Testament'
        else:
            zset = 'Another Testament'
        if zset == 'Another Testament' and not bSaints:
            break
        else:
            if not prev:
                result += f"</ul><ul><h2>{zset}</h2>\n"
                prev = cols
            if not cols[0] == prev[0] and not cols[1] == prev[1]:
                result += f"</ul><ul><h2>{zset}</h2>\n"
                prev = cols
            if cols[0] == prev[0] and not cols[1] == prev[1]:
                result += f"</ul><ul><h2>{zset}</h2>\n"
                prev = cols
            result += f"<li>{LinkBook(zname)}</li>\n"

    result += "</ul>\n"
    result += "</div>\n" # scrlbks
    return result


def FrmBook(curs, book, style, zid):
    ''' The main book view. No Ajax. '''
    res = curs.execute(f"SELECT ID from SqlBooks \
WHERE BOOK LIKE '%{book}%' LIMIT 1;")
    bookid = 1
    try:
        zrow = res.fetchone()
        if zrow:
            bookid = zrow[0]
    except Exception as ex:
        print(ex)
        bookid = 1
    res = curs.execute(f"SELECT BookChapterID, BookVerseID, \
Verse, ID FROM SqlTblVerse WHERE BookID={bookid} ORDER BY ID;")
    result = f"<div class='{style}' id='{zid}'>\n"
    result += f"<h3>{book}</h3>"
    for book in res.fetchall():
        result += f"<p>{LinkVerse(book[3])} {book[0]}:{book[1]} {book[2]}</p>"
    result += "</div>\n"
    return result


def FrmSierraVerse(curs, verse, zclass):
    ''' Extract an in-context reading AROUND a Sierra Verse number.
    Input: Sierra Verse.
    Output: Lines before, and after, the veris. Verse is embolden.
    '''
    res = curs.execute(f"SELECT BookID from SqlTblVerse WHERE ID = {verse} LIMIT 1;")
    bookid = 1; book = None
    try:
        zrow = res.fetchone()
        if zrow:
            bookid = zrow[0]
            book = getBookName(curs, bookid)
    except Exception as ex:
        print(ex)
        bookid = 1
    vstart = int(verse, 10) - 3
    if vstart <= 0:
        vstart = 1
    res = curs.execute(f"SELECT BookChapterID, BookVerseID, \
Verse, ID FROM SqlTblVerse WHERE BookID = {bookid} and ID >= {vstart} ORDER BY ID;")
    result = f"<div class='{zclass}'>\n"
    result += f"<h3>{book}</h3>"
    for book in res.fetchall():
        if int(book[3]) == int(verse):
            result += f"<p>{LinkVerse(book[3])} <b>{book[0]}:{book[1]} {book[2]}</b></p>"
        else:
            result += f"<p>{LinkVerse(book[3])} {book[0]}:{book[1]} {book[2]}</p>"
    result += "</div>\n"
    return result


def FrmQuotes(curs, book, style, zAjaxD):
    result = f"<div class='{style}' id='{zAjaxD}'>\n"
    result += f"<h3>Bookmarks</h3>"
    result += "</div>\n"
    return result


def decode(data):
    ''' Eliminate the overhead, and support a None '''
    if isinstance(data, dict):
        return data
    zsave = dict()
    if not data:
        return zsave
    for key in data:
        ukey = key
        uval = data[key].value
        zsave[ukey] = uval
    return zsave


def DoAjaxBookmark(curs, pkVerse):
    res = curs.execute(f"SELECT BookID, BookChapterID, BookVerseID from SqlTblVerse WHERE ID={pkVerse} LIMIT 1;")
    if not res:
        return f"Error: Unable to locate Sierra Verse {pkVerse}"
    zBook = res.fetchone()
    res = curs.execute(f"SELECT Book from SqlBooks WHERE ID={zBook[0]} LIMIT 1;")
    if not res:
        return f"Error: Unable to locate Sierra Book {zBook[0]}"
    zName = res.fetchone()
    zName = zName[0]
    cols = zName.split('.')
    zName = cols[2]
    result = f"<label onclick='Ax(\"?xrecall={pkVerse}\", \"xbook\")'>@{pkVerse}: {zName} {zBook[1]}:{zBook[2]}</label></br>"
    return result

def DoAjaxRecall(curs, verse):
    return FrmSierraVerse(curs, verse, '')

def DoAjaxBook(curs, book):
    return FrmBook(curs, book, 'noona', 'xbook')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0].lower()] = row[idx]
    return d

if __name__ == '__main__':
    cgitb.enable()
    formMenu   = FormMenu()
    formLookup = FormLookup()
    formSearch = FormSearch()
    data = cgi.FieldStorage()
    data = decode(data)
    zbook = "Genesis"
    zverse= None

    conn = sqlite3.connect("cgi-bin/biblia.sqlt3")
    # conn.row_factory = dict_factory
    curs = conn.cursor()

    if not data:
        print("Welcome!")
    else:
        print(data, file=sys.stderr)
        if formMenu.can_exec(data):
            print(formMenu.exe_cgi_form(data, curs))
            quit()
        if formLookup.can_exec(data):
            print(formLookup.exe_cgi_form(data, curs))
            quit()
        if formSearch.can_exec(data):
            print(formSearch.exe_cgi_form(data, curs))
            quit()
        if 'book' in data:
            zbook  = data['book']
            zverse = None
        if 'verse' in data:
            zbook  = None
            zverse = data['verse']
        if 'xbook' in data:
            print(DoAjaxBook(curs, data['xbook']))
            quit()
        if 'xbkmrk' in data:
            print(DoAjaxBookmark(curs, data['xbkmrk']))
            quit()
        if 'xrecall' in data:
            print(DoAjaxRecall(curs, data['xrecall']))
            quit()
        #if 'xmenu' in data:
        #    print(DoAjaxMenu(curs, data['xmenu']))
        #    quit()
            
    if not bSaints:
        zTitle = "The Classic Scriptures (KJV)"
    else:
        zTitle = "The Sierra Bible"

    chunk = Chunk()
    page = "<html>\n"
    page += "<head>\n"
    page += "<script>"
    page += chunk.get_script()
    page += AjaxStuff
    page += "</script>"
    page += f"<title>{zTitle}</title>"
    page += "<style type='text/css'>\n"
    page += "body {font-family:'Tahoma',sans-serif;font-weight:400;color:#347C17;background-color:rgb(250,250,210);font-size:110%;}"
    page += ".message {font-weight:450;color:#ffffff}"
    page += ".numin   {position:absolute;font-weight:450;width:80px;left:200px;}"
    page += ".scrl, .scrlcite, .scrltome, .scrlbks {height:500px;overflow-y:scroll;}"
    page += ".scrlbks {}"
    page += ".scrltome{}"
    page += ".scrlcite{}"
    page += ".zshape, .eor .zmenu, .zbtn, .zpage, .zcite, .zbooks, .zbook {border-radius:25px;background-color:#d3d3d3;}"
    page += ".zpage  {width:100pct;left:10px;height:100pct;padding:20px;margin:25px;background-color:#f0f0f0;}"
    page += ".zbooks, .zcite {width:300px;padding:10px;}"
    page += ".zbook  {width:400px;padding:20px;}"
    page += ".zmenu  {width:1000px;}"
    page += ".zbtn {padding:12px;margin:20px;background-color:white;}"
    page += ".xlink {text-decoration: underline;}"
    page += ".eor   {border-style=solid;background-color:rgb(250,250,210)}"
    page += "</style>\n"
    page += "</head>\n"
    page += "<body>\n"
    page += chunk.get_html()
    page += "<div class='zpage' id='xpage'>\n"    # zpage
    page += "<table><tr><td>"
    page += formMenu.get_html()     # table.zmenu
    page += "</td></tr><tr>"
    page += "</table>"                 # table.zmenu
    page += "<table><tr>" 
    page += "<td class='zbooks'>\n"    # zbooks
    page += FrmBooks(curs, 'scrlbks')
    page += "</td>\n"                  # zbooks
    page += "<td class='zbook'>\n"     # zbook
    if zbook:
        page += FrmBook(curs, zbook, 'scrltome', 'xbook')
    elif zverse:
        page += FrmSierraVerse(curs, zverse, 'scrltome')
    page += "</td>\n"                  # zbook
    page += "<td class='zcite'>\n";    # zcite
    page += FrmQuotes(curs, zbook, 'scrlcite', 'xbkmrk')
    page += "</td>\n"                  # zcite
    page += "</tr></table>"
    page += "</div>\n"                 # zpage
    page += "</body>\n"
    page += "</html>\n"
    print(page)
