from .. import mailsender
from smtplib import SMTPException
from flask import current_app, render_template
from flask_mail import Message
import os


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    try:
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mailsender.send(msg)
        return True
    except SMTPException:
        current_app.logger.error("Error sending mail")
        return False
