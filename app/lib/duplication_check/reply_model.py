class Reply:
    rpid = 0
    type_id = 0
    mid = 0
    oid = 0
    ctime = 0
    m_name = ""
    content = ""
    like_num = 0

    def keys(self):
        return ['rpid', 'type_id', 'mid', 'oid', 'ctime', 'm_name', 'content', 'like_num']

    def __getitem__(self, item):
        return getattr(self, item)
