import datetime

import peewee

from . import DEFAULT_FOUND_MESSAGE

db = peewee.SqliteDatabase("chats.db")


class User(peewee.Model):
    telegram_id = peewee.IntegerField(unique=True, index=True)
    last_checked = peewee.DateTimeField(default=datetime.datetime.now)
    is_in_club = peewee.BooleanField()
    full_name = peewee.CharField(default="")
    club_slug = peewee.CharField(default="")

    class Meta:
        database = db


class Chat(peewee.Model):
    telegram_id = peewee.IntegerField(unique=True, index=True)
    configured_by = peewee.ForeignKeyField(User)
    found_message = peewee.TextField(default=DEFAULT_FOUND_MESSAGE)
    ban_not_found_user = peewee.BooleanField(default=False)

    class Meta:
        database = db


def create_tables() -> None:
    db.create_tables([User, Chat])
