import os
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import send_file, send_from_directory

FILES_DIRECTORY = 'reports_temp'
ALLOWED_EXTENSIONS = ['xlsx', 'pdf']


def verify_required_keys(data, trusted_keys):

    err_missing_key = {
                    "required_keys": trusted_keys,
                    "sended_keys": list(data.keys())
                }

    for key in trusted_keys:
        if key not in data.keys():
            raise KeyError(err_missing_key)


def verify_allowed_keys(data, allowed_keys):

    err_missing_key = {
                    "allowed_keys": allowed_keys,
                    "sended_keys": list(data.keys())
                }

    for key in data.keys():
        if key not in allowed_keys:
            raise KeyError(err_missing_key)


def send_mail(mail_to_send, subject, attachments):

    # VARIAVEIS DE AMBIENTE
    fromaddr = os.getenv('APP_MAIL')
    mail_pass = os.getenv('MAIL_PASS')
    mail_host = os.getenv('HOST')
    mail_port = os.getenv('PORT')


    email = MIMEMultipart()

    # CONFIG MAIL
    email['From'] = fromaddr
    email['To'] = mail_to_send
    email['Subject'] = f'Relatório {subject}'

    # CORPO DO EMAIL
    message = """
        Segue em anexo o relatório solicitado.

        Att.

        Equipe Simple-Budget.
    """
    email.attach(MIMEText(message, "plain"))

    for item in attachments:

        # ANEXA O(S) ARQUIVO(S)
        filename = item
        path = f'app/reports_temp/{filename}'

        attachment = open(path, 'rb')
        x = MIMEApplication(attachment.read(), Name=filename)
        encoders.encode_base64(x)
        x.add_header('Content-Disposition', 'attachment', filename=filename)
        email.attach(x)

    # ENVIO
    mailer = smtplib.SMTP(mail_host, mail_port)
    mailer.starttls()
    mailer.login(email['From'], mail_pass)
    text = email.as_string()
    mailer.sendmail(email['From'], email['To'], text)
    mailer.quit()


def download_file(file_name:str):

    file_path = f'{FILES_DIRECTORY}/{file_name}'

    if not verify_existing_file(file_name):
        raise FileNotFoundError(
            {
                "error": "File not found!"
            }
        )
    return send_from_directory(
        directory="/reports_temp/report.pdf",
        path=file_name,
        as_attachment=True
    )


def verify_existing_file(file_name:str):

    *_, files_list = next(os.walk(f'app/{FILES_DIRECTORY}'))
    return file_name in files_list

