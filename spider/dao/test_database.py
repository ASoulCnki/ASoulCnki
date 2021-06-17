from spider.dao.engine import DBSession
from spider.dao.models import UserDynamic

if __name__ == '__main__':
    session = DBSession()
    # 创建新User对象:
    new_dynamic = UserDynamic()
    new_dynamic.dynamic_id = 1112
    new_dynamic.type_id = 17
    new_dynamic.oid = 11
    # 添加到session:
    exists = False
    result = session.query(UserDynamic).filter(UserDynamic.dynamic_id == 1112).all()
    print(result)

    if result is None or len(result) == 0:
        session.add(new_dynamic)
        # 提交即保存到数据库:
        session.commit()
    # 关闭session:
    session.close()
