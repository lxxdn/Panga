import yaml
import smtplib
from imaplib import IMAP4_SSL
from imaplib import IMAP4
from email.mime.text import MIMEText
from email.header import Header
import email
import re


class Mail(object):
    CONFIG_FILE_PATH = 'secrets.yml'

    def __init__(self):
        with open(Mail.CONFIG_FILE_PATH, 'r') as file:
            self.config = yaml.load(file)['mail']

    def send(self, to_list, subject, content):
        host = self.config['notifier']['host']
        mail_account = self.config['notifier']['email']
        password = self.config['notifier']['password']

        smtp = smtplib.SMTP_SSL(host)
        smtp.login(mail_account, password)

        msg = MIMEText(content)
        msg['Content-Type'] = 'Text/HTML'
        msg['Subject'] = Header(subject, 'utf-8')
        msg['To'] = to_list
        msg['From'] = mail_account

        try:
            smtp.sendmail(mail_account, to_list, msg.as_string())
        finally:
            smtp.close()

    def receive(self):
        host = self.config['receiver']['host']
        mail_account = self.config['receiver']['email']
        password = self.config['receiver']['password']
        pattern = re.compile(r'\[[pP]anga\]')

        contents = []

        try:
            imap = IMAP4_SSL(host, 993)
            imap.login(mail_account, password)

            imap.select('INBOX')
            (retcode, msg_codes) = imap.search(None, '(UNSEEN)')
            if retcode == 'OK' and msg_codes:
                msg_codes = ' '.join([code.decode()
                                      for code in msg_codes]).split(' ')
                for code in msg_codes:
                    if not code:
                        continue
                    _, data = imap.fetch(code, '(RFC822)')
                    msg = email.message_from_bytes(data[0][1])
                    (subject,
                     encode) = email.header.decode_header(msg['Subject'])[0]

                    try:
                        subject = subject.decode(encode)
                    except AttributeError:
                        pass

                    if pattern.match(subject):
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(
                                    None, decode=True).decode(
                                        part.get_content_charset())
                                print(body)
                                contents.append(body)
                                imap.store(code, '+FLAGS', '\Seen')
        except IMAP4.error:
            print("Credential error!! Please check your email configurations")

        finally:
            if imap.state == 'SELECTED':
                imap.close()

        return contents


if __name__ == "__main__":
    m = Mail()
    content = m.receive()
    print(content)
