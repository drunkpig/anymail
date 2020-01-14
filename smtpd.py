import asyncio
import mimetypes,base64

from aiosmtpd.controller import Controller
import os, time, email


class DataHandler(object):

    def get_charset(self, headers):
        for k,v in headers:
            if 'content-type' == k.lower():
                return v[v.rfind("=")+2:-1]
        return 'utf-8'

    async def __parse_mail(self,msg):
        counter = 0
        html_mail_content = ""
        for part in msg.walk():
            charset = self.get_charset(part._headers)
            # multipart/* are just containers
            content_type = part.get_content_type().lower()
            payload = part.get_payload(decode=True)

            if 'multipart' in content_type:
                continue
            elif 'text/plain' in content_type:
                c = payload.decode(charset)
                html_mail_content += c
            elif 'text/html' in content_type:
                c = payload.decode(charset)
                html_mail_content += c
            else:
                # Applications should really sanitize the given filename so that an
                # email message can't be used to overwrite important files
                filename = part.get_filename()
                if not filename:
                    ext = mimetypes.guess_extension(part.get_content_type())
                    if not ext:
                        # Use a generic bag-of-bits extension
                        ext = '.bin'
                    filename = f'part-{counter}{ext}'
                counter += 1
                with open(os.path.join('/temp/mailbox/', filename), 'wb') as fp:
                    fp.write(part.get_payload(decode=True))

    async def save_mail(self, _from, to, msg):
        await self.__parse_mail(msg)

    async def handle_DATA(self, server, session, envelope):
        _from = envelope.mail_from
        _to = envelope.rcpt_tos[0]
        print(f"FROM<{_from}> TO<{_to}>")
        s = envelope.content.decode('utf8', errors='replace')
        msg = email.message_from_string(s)
        await self.save_mail(_from, _to, msg)

        return '250 Message accepted for delivery'


maildir_path=os.path.expanduser("~/mailbox")
loop = asyncio.get_event_loop()
controller = Controller(DataHandler(), loop=loop, hostname='0.0.0.0', port=25)
controller.start()


while True:
    time.sleep(10)
