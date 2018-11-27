from peewee import *

sqlite_db = SqliteDatabase('sqlite.db', pragmas={'journal_mode': 'wal'})


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class User(BaseModel):
    userid = TextField(unique=True)
    username = TextField()


if __name__ == '__main__':
    if sqlite_db.connect():
        try:
            BaseModel.create_table()
            User.create_table()
        except NotImplementedError:
            pass
