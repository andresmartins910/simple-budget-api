import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
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

def send_mail(mail_to_send, attachment, subject, mail_body):

    fromaddr = os.getenv('APP_MAIL')
    mail_pass = os.getenv('MAIL_PASS')
    mail_host = os.getenv('HOST')
    mail_port = os.getenv('PORT')

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = mail_to_send
    msg['Subject'] = subject

    body = mail_body
    msg.attach(MIMEText(body, 'plain'))

    filename = "File_name_with_extension"

    attachment = open("Path of the file", "rb")

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP(mail_host, mail_port)

    s.starttls()

    s.login(fromaddr, mail_pass)
    text = msg.as_string()
    s.sendmail(fromaddr, mail_to_send, text)

    s.quit()

def test_pandas(data_json):

    df = pd.read_json(data_json, orient='records')

    print(f'{df=}')
    ...


def get_report_to_pdf(type:int):
    # Instantiating a Page
    page = es.Page(title="Research")

    # Page layout hierarchy:
    # Page -> Section -> Row -> Column -> Content

    # Add or update content
    # Keys are used as titles
    page["Introduction"]["Part One"]["Item A"] = "app/services/test/content.md"
    page["Introduction"]["Part One"]["Item B"] = "app/services/test/image1.jpg"

    # Add content without a title
    page["Introduction"]["Part One"][""] = "Hello, World!"

    # Replace child at index - useful if no title given
    page["Introduction"]["Part One"][-1] = "teste"

    # Set content and return input object
    # Useful in Jupyter Notebook as it will be displayed in cell output
    page["Methodology"]["Part One"]["Item A"] << "dolor sit amet"

    # Set content and return new layout
    page["Methodology"]["Part Two"]["Item B"] >> "foobar"

    # Show document structure
    # page.tree()

    # Remove content
    del page["Methodology"]["Part One"]["Item A"]
    del page.methodology.part_two.item_b

    # Access existing content as an attribute
    page.introduction.part_one.item_a = "app/services/test/image2.jpg"
    page.introduction.part_one.tree()

    # Save the document
    if type == 0:
        page.save_html("app/services/test/report.html")
        return "", 200
    else:
        page.save_pdf("app/services/test/report.pdf")
        return "", 200
