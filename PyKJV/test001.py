if __name__ == "__main__":
    from verse import Verse
    from sierra_dao import SierraDAO
    assert(SierraDAO.IsValidVerse('Gene:1:1'))
    assert(SierraDAO.IsValidVerse('gEnE:1:1'))
    assert(SierraDAO.IsValidVerse('Gene:0:1') == False)
    assert(SierraDAO.IsValidVerse('Gene:1:0') == False)
    dao = SierraDAO.GetDAO()
    books = list(dao.list_books())
    assert('Genesis' in books)
    v = Verse()
    test = dao.search("verse LIKE '%PERFECT%'")
    assert (len(list(test)) == 124)
    assert (dao.get_sierra(123)['sierra'] == '123')
    assert (dao.get_sierra(123)['sierra'] == '123')
    zdict = dao.list_book_table()
    zbooks = list(zdict)
    assert (len(zbooks) == 81)
