from flask import current_app
from flask_mail import Message

from Norman.extensions import mailer
from Norman.settings import MailerConfig


def send_email(subject, recipients, text_body=None, html_body=None, **kwargs):
    sender = MailerConfig.MAIL_USERNAME
    recipients = handle_recipients(recipients)
    current_app.logger.info("send_email(subject='{subject}', recipients=['{recp}'], text_body='{txt}')".format(sender=sender, subject=subject, recp=recipients, txt=text_body))
    msg = Message(subject, sender=sender, recipients=recipients, **kwargs)
    msg.body = text_body
    msg.html = html_body

    current_app.logger.info("Message(to=[{m.recipients}], from='{m.sender}')".format(m=msg))
    mailer.send_message(
        sender,
        recipients,
        subject, html=msg.html
    )
    # _send_async_email(current_app.name, msg)


def handle_recipients(recipients):
        if isinstance(recipients, list):
            recipients = recipients
        return recipients
