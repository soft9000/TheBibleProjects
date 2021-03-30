if __name__ == "__main__":
    from verse import Verse
    from sierra_dao import SierraDAO
    dao = SierraDAO.GetDAO()
    v = Verse()
    test = dao.search("verse LIKE '%PERFECT%'")
    assert (len(list(test)) == 124)
    assert (dao.get_sierra(123)['sierra'] == '123')
    assert (dao.get_sierra(123)['sierra'] == '123')
    zdict = dao.list_book_table()
    zbooks = list(zdict)
    assert (len(zbooks) == 81)
