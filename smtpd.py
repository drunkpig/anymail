import asyncio
import mimetypes
import tempfile

from aiosmtpd.controller import Controller
import os, time, email


class DataHandler(object):

    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos[0])
        print('Message data:\n')
        s = envelope.content.decode('utf8', errors='replace')
        msg = email.message_from_string(s)
        simplest = msg.get_body(preferencelist=('plain', 'html'))
        print()
        print(''.join(simplest.get_content().splitlines(keepends=True)[:3]))

        richest = msg.get_body()
        partfiles = {}
        mail_content = ""
        if richest['content-type'].maintype == 'text':
            if richest['content-type'].subtype == 'plain':
                for line in richest.get_content().splitlines():
                    mail_content += line
            elif richest['content-type'].subtype == 'html':
                mail_content += richest
            else:
                print("Don't know how to display {}".format(richest.get_content_type()))
        elif richest['content-type'].content_type == 'multipart/related':
            body = richest.get_body(preferencelist=('html'))
            for part in richest.iter_attachments():
                fn = part.get_filename()
                if fn:
                    extension = os.path.splitext(part.get_filename())[1]
                else:
                    extension = mimetypes.guess_extension(part.get_content_type())
                with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as f:
                    f.write(part.get_content())
                    # again strip the <> to go from email form of cid to html form.
                    partfiles[part['content-id'][1:-1]] = f.name
        else:
            print("Don't know how to display {}".format(richest.get_content_type()))
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            # The magic_html_parser has to rewrite the href="cid:...." attributes to
            # point to the filenames in partfiles.  It also has to do a safety-sanitize
            # of the html.  It could be written using html.parser.
            f.write(magic_html_parser(body.get_content(), partfiles))



        return '250 Message accepted for delivery'


maildir_path=os.path.expanduser("~/mailbox")
loop = asyncio.get_event_loop()
controller = Controller(DataHandler(maildir_path), loop=loop, hostname='0.0.0.0', port=25)
controller.start()

while True:
    time.sleep(10)

