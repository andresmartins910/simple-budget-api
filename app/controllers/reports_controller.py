from email.policy import HTTP
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.models.budgets_model import BudgetModel
from app.models.users_model import UserModel

from flask import request, current_app

from http import HTTPStatus

import os

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


@jwt_required()
def pdf_to_mail():
    data = request.args

    current_user = get_jwt_identity()

    accepted_args = []

    # budgets = BudgetModel.query.filter_by(user_id = current_user["id"]).all()
    # print(budgets)

    for i in data:
        accepted_args.append(i)

    
    if(accepted_args):
        if("year" in accepted_args and "category_id" in accepted_args):
            print(data["year"], data["category_id"])


        elif("year" in accepted_args):
            try:
                year_ok = datetime.strptime(data["year"], "%Y")

            except:
                return {"error": "year must be format 'YYYY'"}, HTTPStatus.BAD_REQUEST

            year = data["year"]

            years_first_day = f"01/01/{year}"
            years_last_day = f"31/12/{year}"

            expenses = current_app.db.session.query(ExpenseModel).select_from(ExpenseModel).join(BudgetModel).join(UserModel).filter(UserModel.id == current_user['id']).filter(ExpenseModel.created_at.between(years_first_day, years_last_day)).all()

            total, categories = normalize_amount(expenses)

            new_amount = []

            for i in total:
                new_amount.append(i["amount"])

            if(len(categories) > 0 and len(new_amount) > 0):
                with PdfPages("expenses.pdf") as pdf:
                    # plt.plot(name, amount)
                    plt.bar(categories, new_amount)
                    plt.xlabel("Categorias")
                    plt.ylabel("Despesas")

                    plt.title(f"Despesas do Ano de {year}")

                    pdf.savefig()
                    plt.close()

                    return {
                        "expenses": expenses
                    }, 201
            
            return {
                "error": "Insufficient data"
            }, HTTPStatus.BAD_REQUEST


        elif("category_id" in accepted_args):
            expenses = current_app.db.session.query(ExpenseModel).select_from(ExpenseModel).join(CategoryModel).filter(ExpenseModel.category_id == CategoryModel.id).filter(CategoryModel.id == data["category_id"]).all()

            total, categories = normalize_amount(expenses)

            new_amount = []

            for i in total:
                new_amount.append(i["amount"])

            if(len(categories) > 0 and len(new_amount) > 0):
                x = []

                for i in expenses:
                    x.append(i.name)

                with PdfPages("expenses.pdf") as pdf:
                    # plt.plot(name, amount)
                    plt.bar(x, new_amount)
                    plt.xlabel("Categorias")
                    plt.ylabel("Despesas")

                    plt.title(f"Despesas da Categoria de {categories[0]}")

                    pdf.savefig()
                    plt.close()

                    send_mail("auhuheuhew@gmail.com")

                    return {
                        "expenses": expenses
                    }, 201

            
            return {
                "error": "Insufficient data"
            }, HTTPStatus.BAD_REQUEST


        elif("initial_date" in accepted_args and "final_date" in accepted_args):
            print(data["initial_date"], data["final_date"])

        else:
            return {
                "error": "Wrong Arguments"
            }, HTTPStatus.BAD_REQUEST



def normalize_amount(expenses):
    amount = []
    categories = []
    total = []

    for i in expenses:
        if(i.category.name in categories):
            for j in total:
                if(i.category.name == j["category"]):
                    j["amount"] = j["amount"] + i.amount

        else:
            amount.append(i.amount)
            categories.append(i.category.name)

            object = {
                "category": i.category.name,
                "amount": i.amount
            }


            total.append(object)

    return total, categories


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

    filename = 'expenses.pdf'
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
