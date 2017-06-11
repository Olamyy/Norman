from flask import render_template

from .mail import send_email


def registration(**kwargs):
    template = render_template('dashboard/admin/confirm-email.html', hospital=kwargs.get('hospital'))
    subject = 'Norman Registration Confirmation'
    recipient = kwargs.get('recipient')
    return send_email(subject, recipient, html_body=template)