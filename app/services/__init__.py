import os
import smtplib
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import esparto as es
import pandas as pd


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


def test_pandas(data_json):

    df = pd.read_json(data_json, orient='records')

    print(f'{df=}')
    ...


def send_mail(mail_to_send):

    # VARIAVEIS DE AMBIENTE
    fromaddr = os.getenv('APP_MAIL')
    mail_pass = os.getenv('MAIL_PASS')
    mail_host = os.getenv('HOST')
    mail_port = os.getenv('PORT')


    email = MIMEMultipart()

    # CONFIG MAIL
    email['From'] = fromaddr
    email['To'] = mail_to_send
    email['Subject'] = 'Relatório'

    # CORPO DO EMAIL
    message = """
        Segue em anexo o relatório solicitado.

        Att.

        Equipe Simple-Budget.
    """
    email.attach(MIMEText(message, "plain"))

    # ANEXA O ARQUIVO
    filename = 'report.pdf'
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



import os
from flask import send_from_directory


FILES_DIRECTORY = 'app/reports'
ALLOWED_EXTENSIONS = ['xlsx', 'pdf']


def download_file(file_name:str):
    ext = get_extension_file(file_name)

    file_path = f'.{FILES_DIRECTORY}/{ext}'

    if not verify_existing_file(file_name, ext):
        raise FileNotFoundError(
            {
                "error": "File not found!"
            }
        )
    return send_from_directory(
        directory=file_path,
        path=file_name,
        as_attachment=True
    )

def verify_existing_file(file_name:str, ext:str):

    *_, files_list = next(os.walk(f"{FILES_DIRECTORY}/{ext}"))
    return file_name in files_list

def get_extension_file(file_name:str):
    ext = file_name.split('.')[-1]

    if not ext in ALLOWED_EXTENSIONS:
        raise TypeError(
            {
                "error": f"'.{ext}' type files are not allowed in report."
            }
        )
    return ext