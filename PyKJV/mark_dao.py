from sierra_dao import SierraDAO

class BookMark:
    ''' Model / Data Model '''
    m_id = 0
    m_start = 0
    m_end = 0
    m_user = 0

    def __init__(self, start, end, zid=0, user=0):
        self.m_id = zid
        self.m_start = start
        self.m_end = end
        self.m_user = user


class BookMarks:
    ''' Controller / API '''
    @staticmethod
    def Read(user=None) -> list():
        ''' Get all of the BookMarks() for the default / user '''
        if not user:
            user = 0
        cmd = f"SELECT ID, SierraStart, SierraEnd from UserSelects \
            WHERE UserID = {user};"
        conn = SierraDAO.Connect()
        res = conn.execute(cmd)
        results = list()
        zrow = res.fetchone()
        while zrow:
            results.append(BookMark(zrow[1], zrow[2], zrow[0], user))
            zrow = res.fetchone()
        return results 

    @staticmethod
    def Sync(bmk) -> bool:
        if not isinstance(bmk, BookMark):
            return False
        conn = SierraDAO.Connect()
        res = None
        if bmk.m_id == 0:
            cmd = f"INSERT INTO UserSelects (SierraStart, SierraEnd, UserID) \
                VALUES ({bmk.m_start}, {bmk.m_end}, {bmk.m_user});"
            conn = SierraDAO.Connect()
            res = conn.execute(cmd)
        else:
            cmd = f"UPDATE UserSelects SET SierraStart = {bmk.m_start}, SierraEnd = {bmk.m_end}, UserID = {bmk.m_user} WHERE ID = {bmk.m_id};"
            res = conn.execute(cmd)
        if res:
            conn.commit()
        return False
    
    @staticmethod
    def Delete(items, user=None) -> bool:
        ''' Delete a BookMark() or a list() of same.
        Returns FALSE on error. '''
        if isinstance(items, BookMark):
            hole = items
            items = [hole]
        try:
            conn = SierraDAO.Connect()
            for item in items:
                if not isinstance(item, BookMark):
                    return False
                cmd = f"DELETE FROM UserSelects WHERE ID={item.m_id};"
                res = conn.execute(cmd)
            if res:
                conn.commit()
            return True
        except:
            pass
        return False