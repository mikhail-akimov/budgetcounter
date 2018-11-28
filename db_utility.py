from models import *

db = sqlite_db.connect()


def check_user(userid):
    if User.select().where(User.userid == userid):
        result = True
    else:
        result = False
    return result


def add_user(user_id, user_name):
    user = User.create(userid=user_id, username=user_name, force_insert=True)
    return user

