import asyncio
import mailparser

from aiosmtpd.controller import Controller
import os, time


class DataHandler(object):

    async def save_mail(self, _from, to, msg):
        await self.__parse_mail(msg)

    def parse_test(self, raw_mail):
        mail = mailparser.parse_from_string(raw_mail)

    async def handle_DATA(self, server, session, envelope):
        _from = envelope.mail_from
        _to = envelope.rcpt_tos[0]
        print(f"FROM<{_from}> TO<{_to}>")
        s = envelope.content.decode('utf8', errors='replace')
        self.parse_test(s)

        return '250 Message accepted for delivery'


maildir_path=os.path.expanduser("~/mailbox")
loop = asyncio.get_event_loop()
controller = Controller(DataHandler(), loop=loop, hostname='0.0.0.0', port=25)
controller.start()


while True:
    time.sleep(10)
