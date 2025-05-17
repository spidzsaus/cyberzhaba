import os
import datetime

import discord

from app import config
from app.db.models import SqlUser, SqlMailbox
from app.entities.users import User
from app.db import database


class Mailbox:
    def __init__(
        self, sql_mailbox: SqlMailbox
    ):
        self.id = sql_mailbox.id
        self.domain = sql_mailbox.domain
        self.local_part = sql_mailbox.local_part
        self.registered_at = sql_mailbox.registered_at

    @classmethod
    def by_id(mailbox_id: int):
        sql_mailbox = database.session().get(SqlMailbox, mailbox_id)
        if not sql_mailbox:
            raise NameError(f"mailbox {mailbox_id} does not exist")
        
        return Mailbox(sql_mailbox)

    @classmethod
    def create(self, user_id: int, domain: str, local_part: str):
        db_sess = database.session()
        sql_mailbox = db_sess.query(SqlMailbox).filter(
            SqlMailbox.local_part == local_part,
            SqlMailbox.domain == domain
        ).first()
        if sql_mailbox:
            raise NameError(f"mailbox {local_part}@{domain} already exists!")

        sql_mailbox = SqlMailbox(
            user=user_id,
            domain=domain,
            local_part=local_part,
            registered_at=datetime.datetime.now(tz=config.TIMEZONE)
        )
        db_sess.add(sql_mailbox)
        db_sess.commit()

        return Mailbox(sql_mailbox)

    def sql(self) -> SqlMailbox:
        return database.session().get(SqlMailbox, self.id)

    def delete(self):
        db_sess = database.session()
        sql_mailbox = db_sess.get(SqlMailbox, self.id)
        db_sess.delete(sql_mailbox)
        db_sess.commit()
