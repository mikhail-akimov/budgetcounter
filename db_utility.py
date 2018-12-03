from models import *

db = sqlite_db.connect()


def check_user(userid):
    user = User.select().where(User.userid == userid).get()
    if user:
        return user.userid, user.username
    else:
        return False


def add_user(user_id, user_name):
    user = User.create(userid=user_id, username=user_name, force_insert=True)
    return user
