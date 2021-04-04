from sierra_dao import SierraDAO

class BookMark:
    ''' Model / Data Model '''
    m_id = 0
    m_start = 0
    m_end = 0

    def __init__(self, start, end):
        self.m_start = start
        self.m_end = end


class BookMarks:
    ''' Controller / API '''
    @staticmethod
    def GetBookmarks(user=None) -> list():
        pass

    @staticmethod
    def Sync(bmk, user=None) -> bool:
        if not isinstance(bmk, BookMark):
            return False
        if bmk.m_id == 0:
            cmd = f"INSERT INTO UserSelects (SierraStart, SierraEnd, UserID) \
                VALUES ({bmk.m_start}, {bmk.m_end}, {bmk.m_id});"
            conn = SierraDAO.Connect()
            res = conn.execute(cmd)
            conn.commit()
            return True
        return False
