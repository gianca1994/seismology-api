from .. import sendmail
from smtplib import SMTPException
from threading import Thread
from flask import current_app
from flask_mail import Message
import os


def send_email(subject, recipients, text_body, html_body=None):
    message = Message(
        subject=subject,
        sender=current_app.config["FLASKY_MAIL_SENDER"],
        recipients=recipients
    )
    try:
        message.body = text_body

        if html_body:
            message.html = html_body

        sendmail.send(message)

    except SMTPException as error:
        print(str(error))
        return "Mail deliver failed" + str(error)
    return True
