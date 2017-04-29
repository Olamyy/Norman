from flask_mail import Message, Mail
from flask import Flask
from Norman.settings import MailerConfig
from Norman.app import create_app


class NormanMailer(Message):
    def __init__(self, recipient):
        super().__init__(sender=MailerConfig.ADMINS[0])
        self.app = Flask(__name__)
        self.mail = Mail()
        self.recipient_list = recipient
        self.handle_recipients()

    def handle_recipients(self):
        if isinstance(self.recipient_list, list):
            self.recipients = self.recipient_list
        self.add_recipient(self.recipients)

    def send_mail(self, message, message_subject, msg_type='text'):
        msg = Message(message_subject, sender=MailerConfig.ADMINS[0], recipients=self.recipient_list)
        if msg_type == 'text':
            msg.text = message
        elif msg_type == 'html':
            msg.html = message
        self.mail.init_app(self.app).send(msg)

if __name__ == '__main__':
    test = NormanMailer('wapshow01@gmail.com')
    test.send_mail('<b>HTML</b> body',  message_subject='test subject')
