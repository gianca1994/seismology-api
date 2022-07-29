from .. import sendmail
from smtplib import SMTPException
from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
import os


def send_mail(to, subject, template, **kwargs):
    message = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)

    try:
        message.body = render_template(template + '.txt', **kwargs)
        if message.body:
            message.html = render_template(template + '.html', **kwargs)

        sendmail.send(message)
    except SMTPException as e:
        print(str(e))
        return "Mail deliver failed"
    return True
