import mailparser
import sqlite3
from aiosmtpd.controller import Controller
import os, time
from datetime import datetime


class DataHandler(object):

    def __init__(self, mailbox_dir, db_name, table_name):
        self.maildir =os.path.expanduser(mailbox_dir)
        self.db_name = db_name
        self.table_name = table_name
        self.db = f"{self.maildir}/{self.db_name}"
        self.init_db()

    async def save_mail(self, _from, to, tm, raw_mail):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        sql = f"""
            insert into {self.table_name} (`email_from`, `email_to`, `dt`, `email_raw`) values
            (?, ?, ?, ?)
        """
        print(sql)
        cur.execute(sql, (_from, to, tm, raw_mail))
        conn.commit()
        cur.close()
        conn.close()

    async def parse(self, raw_mail):
        mail = mailparser.parse_from_string(raw_mail)
        from_ = mail.from_[0][1]
        to_ = mail.to[0][1]
        tm = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{from_}\t{to_}\t{mail.subject}")
        await self.save_mail(from_, to_, tm, raw_mail)

    async def handle_DATA(self, server, session, envelope):
        s = envelope.content.decode('utf8', errors='replace')
        await self.parse(s)

        return '250 Message accepted for delivery'

    def init_db(self):
        print(f"use db {self.db}")
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        sql = f"""
            create table  if not exists  {self.table_name}(
            id INTEGER  PRIMARY KEY autoincrement,
            email_from   VARCHAR(255),
            email_to  VARCHAR(255),
            dt TEXT,
            email_raw TEXT
            )
        """
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()


if __name__=='__main__':

    try:
        controller = Controller(DataHandler("~/mailbox", 'fake_mail.db', "fake_mail"), hostname='0.0.0.0', port=25)
        controller.start()

        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("smtpd quit!")
