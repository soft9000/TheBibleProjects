if __name__ == "__main__":
    from verse import Verse
    from sierra_dao import SierraDAO
    import mark_dao

    assert SierraDAO.ParseClassicVerse("Genesis:1:1")
    assert SierraDAO.ParseClassicVerse("gEnesis:1:1")
    assert SierraDAO.ParseClassicVerse("Gene:1:1")
    assert SierraDAO.ParseClassicVerse("gEnE:1:1")
    assert SierraDAO.ParseClassicVerse("Gene:0:1") == False
    assert SierraDAO.ParseClassicVerse("Gene:1:0") == False
    dao = SierraDAO.GetDAO()
    books = list(dao.list_books())
    assert "Genesis" in books
    assert dao.get_sierra_book("gEnE", 1, 2) == 2
    v = Verse()
    test = dao.search("verse LIKE '%PERFECT%'")
    assert len(list(test)) == 124
    assert dao.get_sierra(123)["sierra"] == "123"
    assert dao.get_sierra(123)["sierra"] == "123"
    zdict = dao.list_book_table()
    zbooks = list(zdict)
    assert len(zbooks) == 81
    print("Testing Success!")
    bmk = mark_dao.BookMark(15, 99)
    mark_dao.BookMarks.Sync(bmk)
    print("Testing Success!")
    # TODO: Test the BookMarks class signature - Full C.R.U.D ops.
