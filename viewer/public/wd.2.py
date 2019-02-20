# -*- coding: utf-8 -*-
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import time
from email.mime.text import MIMEText
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

target_dir = 'picture'

class sendGmailAttach:
    username, password = 'okkun.noto@gmail.com', 'tomo0406noto'

    def __init__(self, to, sub, body, attach_file):
        host, port = 'smtp.gmail.com', 465
        msg = MIMEMultipart()
        msg['Subject'] = sub
        msg['From'] = self.username
        msg['To'] = to

        # メール本文
        body = MIMEText(body)
        msg.attach(body)

        # 添付ファイルの設定
        attachment = MIMEBase('image', 'jpeg')
        file = open(attach_file['path'], 'rb+')
        attachment.set_payload(file.read())
        file.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=attach_file['name'])
        msg.attach(attachment)

        smtp = smtplib.SMTP_SSL(host, port)
        smtp.ehlo()
        smtp.login(self.username, self.password)
        smtp.mail(self.username)
        smtp.rcpt(to)
        smtp.data(msg.as_string())
        smtp.quit()
        print('ok')

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%sができました' % filename)
        to = 's1632041uh@s.chibakoudai.jp'
        sub = 'test'
        body = 'file send test'
        pathname = 'picture/'+filename
        attach_file = {'name': filename, 'path':pathname}
        sendGmailAttach(to, sub, body, attach_file)

if __name__ in '__main__':
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler, target_dir, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
