from email.policy import HTTP
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from datetime import datetime as dt

from flask_jwt_extended import jwt_required, get_jwt_identity

from app.configs.database import db

from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.models.budgets_model import BudgetModel
from app.models.users_model import UserModel

from flask import request, current_app, jsonify

from http import HTTPStatus

import os

import smtplib
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import Session, Query

REPORTS_TEMP = os.getenv("REPORTS_TEMP")


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
    path = f'app/{REPORTS_TEMP}/{filename}'
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



@jwt_required()
def report_with_filter():

    session: Session = current_app.db.session

    registers: BaseQuery = session.query(ExpenseModel)

    current_user = get_jwt_identity()

    year = request.args.get("year", type=str)
    category_id = request.args.get("category_id", type=int)
    initial_date = request.args.get("initial_date", type=str)
    final_date = request.args.get("final_date", type=str)

    if not year and not category_id and not initial_date and not final_date:

        session: Session = current_app.db.session

        budgets: Query = (
            session.query(BudgetModel)
            .join(UserModel)
            .filter(BudgetModel.user_id == current_user["id"])
            .all()
        )

        budgets_arr = []

        for budget in budgets:

            expenses: Query = (
                session.query(ExpenseModel)
                .join(BudgetModel)
                .join(UserModel)
                .filter(UserModel.id == current_user["id"])
                .filter(ExpenseModel.budget_id == budget.id)
                .all()
            )

            expenses_arr = []

            for expense in expenses:

                categories: Query = (
                    session.query(CategoryModel)
                    .filter(CategoryModel.id == expense.category_id)
                    .first()
                )

                new_expense = {
                    "name": expense.name,
                    "description": expense.description,
                    "amount": expense.amount,
                    "created_at": expense.created_at,
                    "category": categories.name ,
                }

                expenses_arr.append(new_expense)

            new_budget = {
                "month_year": budget.month_year,
                "expenses": expenses_arr
            }

            budgets_arr.append(new_budget)

        data_return = {
            "user": current_user["name"],
            "budgets": budgets_arr
        }

    elif year and not category_id and not initial_date and not final_date:

        try:
            year_ok = dt.strptime(year, "%Y")
        except:
            return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

        years_first_day = f"01/01/{year}"
        years_last_day = f"31/12/{year}"

        registers: Query = (
            registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .filter(UserModel.id == current_user['id'])
            .filter(ExpenseModel.created_at.between(years_first_day, years_last_day))
            .all()
        )

        expenses = []

        for expense in registers:

            new_expense = {
                "name": expense.name,
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
                "budget": expense.budget.month_year,
                "category": expense.category.name
            }

            expenses.append(new_expense)

        data_return = {
            "user": current_user['name'],
            "year": year,
            "expenses": expenses
        }

    elif category_id and not year and not initial_date and not final_date:

        session: Session = db.session

        category = session.query(CategoryModel).get(category_id)

        if not category:
            return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

        registers: Query = (
            registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .join(CategoryModel)
            .filter(UserModel.id == current_user['id'])
            .filter(CategoryModel.id == category_id)
            .all()
        )

        expenses = []

        for expense in registers:

            new_expense = {
                "name": expense.name,
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
                "budget": expense.budget.month_year
            }

            expenses.append(new_expense)

        data_return = {
            "user": current_user['name'],
            "category": category.name,
            "expenses": expenses
        }

    elif category_id and year and not initial_date and not final_date:

        session: Session = db.session

        category = session.query(CategoryModel).get(category_id)

        if not category:
            return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

        try:
            year_ok = dt.strptime(year, "%Y")
        except:
            return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

        years_first_day = f"01/01/{year}"
        years_last_day = f"31/12/{year}"

        registers: Query = (
            registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .join(CategoryModel)
            .filter(UserModel.id == current_user['id'])
            .filter(ExpenseModel.created_at.between(years_first_day, years_last_day))
            .filter(CategoryModel.id == category_id)
            .all()
        )

        expenses = []

        for expense in registers:

            new_expense = {
                "name": expense.name,
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
                "budget": expense.budget.month_year,
                "category": expense.category.name
            }

            expenses.append(new_expense)

        data_return = {
            "user": current_user['name'],
            "year": year,
            "category": category.name,
            "expenses": expenses
        }

    elif initial_date and final_date and not year and not category_id:

        try:
            initial_date_ok = dt.strptime(initial_date, "%d/%m/%Y")
            final_date_ok = dt.strptime(final_date, "%d/%m/%Y")
        except:
            return {"error": "start and end dates must be format 'dd/mm/YYYY'."}, HTTPStatus.BAD_REQUEST

        registers: Query = (
            registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .filter(UserModel.id == current_user['id'])
            .filter(ExpenseModel.created_at.between(initial_date, final_date))
            .all()
        )

        expenses = []

        for expense in registers:

            new_expense = {
                "name": expense.name,
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
                "budget": expense.budget.month_year,
                "category": expense.category.name
            }

            expenses.append(new_expense)

        data_return = {
            "user": current_user['name'],
            "initial_date": initial_date,
            "final_date": final_date,
            "expenses": expenses
        }

    else:
        return jsonify({"error": "This request is not allowed."}), HTTPStatus.BAD_REQUEST


    return jsonify(data_return), HTTPStatus.OK


@jwt_required()
def report_with_filter_by_budget(budget_id):
    session: Session = db.session()

    registers: BaseQuery = session.query(ExpenseModel)
    budget: BudgetModel = BudgetModel.query.filter_by(id=budget_id).first()

    if not budget:
        return {"error": "no data found in database"}

    current_user = get_jwt_identity()

    registers: Query = (
            registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .filter(ExpenseModel.budget_id == budget_id)
            .filter(BudgetModel.id == budget_id)
            .filter(UserModel.id == current_user['id'])
            .all()
        )

    expenses = []

    for expense in registers:
        new_expense = {
            "name": expense.name,
            "description": expense.description,
            "amount": expense.amount,
            "created_at": expense.created_at
        }

        expenses.append(new_expense)

    data_return = {
        "user": current_user['name'],
        "budget": budget.month_year,
        "expenses": expenses
    }

    return jsonify(data_return), HTTPStatus.OK


@jwt_required()
def pdf_to_mail():
    plt.rc("font", size=6)

    data = request.args

    current_user = get_jwt_identity()

    session: Session = current_app.db.session

    registers: BaseQuery = session.query(ExpenseModel)

    accepted_args = []


    for i in data:
        accepted_args.append(i)

    
    if(accepted_args):
        if("year" in accepted_args and "category_id" in accepted_args):
            year = data["year"]
            category_id = data["category_id"]

            registers: Query = session.query(ExpenseModel)

            session: Session = db.session

            category = session.query(CategoryModel).get(category_id)

            if not category:
                return {"error": "category not found."}, HTTPStatus.BAD_REQUEST
                
            try:
                year_ok = dt.strptime(year, "%Y")
            except:
                return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

            years_first_day = f"01/01/{year}"
            years_last_day = f"31/12/{year}"

            registers: Query = (
                registers
                .select_from(ExpenseModel)
                .join(BudgetModel)
                .join(UserModel)
                .join(CategoryModel)
                .filter(UserModel.id == current_user['id'])
                .filter(ExpenseModel.created_at.between(years_first_day, years_last_day))
                .filter(CategoryModel.id == category_id)
                .all()
            )

            expenses = []
            name = []
            amount = []
            title = f"Despesas do Ano de {year} e da Categoria {category.name}"
            xlabel = "Nome das Despesas"

            for expense in registers:
                name.append(expense.name)
                amount.append(expense.amount)

                new_expense = {
                    "name": expense.name,
                    "description": expense.description,
                    "amount": expense.amount,
                    "created_at": expense.created_at,
                    "budget": expense.budget.month_year,
                    "category": expense.category.name
                }

                expenses.append(new_expense)

            if(len(name) > 0 and len(amount) > 0):
                create_pdf_by_category(name, amount, title, xlabel)

                return {
                    "user": current_user['name'],
                    "year": year,
                    "category": category.name,
                    "expenses": expenses
                }, HTTPStatus.OK


        elif("year" in accepted_args):
            try:
                year_ok = dt.strptime(data["year"], "%Y")

            except:
                return {"error": "year must be format 'YYYY'"}, HTTPStatus.BAD_REQUEST

            year = data["year"]

            years_first_day = f"01/01/{year}"
            years_last_day = f"31/12/{year}"

            title = f"Despesas do Ano de {year}"
            xlabel = "Categorias"

            registers: Query = (
                registers
                .select_from(ExpenseModel)
                .join(BudgetModel)
                .join(UserModel)
                .filter(UserModel.id == current_user['id'])
                .filter(ExpenseModel.created_at.between(years_first_day, years_last_day))
                .all()
            )

            total, categories = normalize_amount(registers)

            new_amount = []

            for i in total:
                new_amount.append(i["amount"])

            if(len(categories) > 0 and len(new_amount) > 0):
                create_pdf_by_category(categories, new_amount, title, xlabel)

                return {
                    "user": current_user['name'],
                    "year": year,
                    "expenses": registers
                }, 201
            
            return {
                "error": "Insufficient data"
            }, HTTPStatus.BAD_REQUEST


        elif("category_id" in accepted_args):
            category_id = data["category_id"]

            session: Session = db.session

            category = session.query(CategoryModel).get(category_id)

            if not category:
                return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

            registers: Query = (
                registers
                .select_from(ExpenseModel)
                .join(BudgetModel)
                .join(UserModel)
                .join(CategoryModel)
                .filter(UserModel.id == current_user['id'])
                .filter(CategoryModel.id == category_id)
                .all()
            )

            expenses = []
            name = []
            amount = []
            title = f"Despesas da Categoria {category.name}"
            xlabel = "Nome das Despesas"

            for expense in registers:
                name.append(expense.name)
                amount.append(expense.amount)

                new_expense = {
                    "name": expense.name,
                    "description": expense.description,
                    "amount": expense.amount,
                    "created_at": expense.created_at,
                    "budget": expense.budget.month_year
                }

                expenses.append(new_expense)


            if(len(name) > 0 and len(amount) > 0):
                create_pdf_by_category(name, amount, title, xlabel)

                return {
                    "user": current_user['name'],
                    "category": category.name,
                    "expenses": expenses
                }

            return {
                "error": "Insufficient data"
            }, HTTPStatus.BAD_REQUEST


        elif("initial_date" in accepted_args and "final_date" in accepted_args):
            initial_date = data["initial_date"]
            final_date = data["final_date"]
            
            try:
                initial_date_ok = dt.strptime(initial_date, "%d/%m/%Y")
                final_date_ok = dt.strptime(final_date, "%d/%m/%Y")
            except:
                return {"error": "start and end dates must be format 'dd/mm/YYYY'."}, HTTPStatus.BAD_REQUEST

            registers: Query = (
                registers
                .select_from(ExpenseModel)
                .join(BudgetModel)
                .join(UserModel)
                .filter(UserModel.id == current_user['id'])
                .filter(ExpenseModel.created_at.between(initial_date, final_date))
                .all()
            )

            total, categories = normalize_amount(registers)
            title = f"Despesas da data entre {initial_date} e {final_date}"
            xlabel = "Categorias"

            new_amount = []

            for i in total:
                new_amount.append(i["amount"])


            if(len(categories) > 0 and len(new_amount) > 0):
                create_pdf_by_category(categories, new_amount, title, xlabel)

                return {
                    "user": current_user['name'],
                    "initial_date": initial_date,
                    "final_date": final_date,
                    "expenses": registers
                }

            return {
                "error": "Insufficient data or Wrong Data"
            }, HTTPStatus.BAD_REQUEST

        else:
            return {
                "error": "Wrong Arguments"
            }, HTTPStatus.BAD_REQUEST


@jwt_required()
def pdf_to_mail_by_budget_id(budget_id):
    session: Session = db.session()

    registers: BaseQuery = session.query(ExpenseModel)
    budget: BudgetModel = BudgetModel.query.filter_by(id=budget_id).first()

    if not budget:
        return {"error": "no data found in database"}

    current_user = get_jwt_identity()

    registers: Query = (
        registers
        .select_from(ExpenseModel)
        .join(BudgetModel)
        .join(UserModel)
        .filter(ExpenseModel.budget_id == budget_id)
        .filter(BudgetModel.id == budget_id)
        .filter(UserModel.id == current_user['id'])
        .all()
    )

    amount = []

    total, categories = normalize_amount(registers)
    title = f"Despesas do Budget de {budget.month_year}"
    xlabel = "Categorias"

    for i in total:
        amount.append(i["amount"])


    if(len(categories) > 0 and len(amount) > 0):
        create_pdf_by_category(categories, amount, title, xlabel)
        # send_mail("auhuheuhew@gmail.com")

        return {
            "user": current_user['name'],
            "budget": budget.month_year,
            "expenses": total
        }, HTTPStatus.OK

    return {
        "error": "Insufficient data"
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
                "name": i.name,
                "description": i.description,
                "created_at": i.created_at,
                "category": i.category.name,
                "amount": i.amount
            }

            total.append(object)

    return total, categories


def create_pdf_by_category(categories, amount, title, xlabel):
    os.makedirs(f"app/{REPORTS_TEMP}", exist_ok=True)

    with PdfPages(f"app/{REPORTS_TEMP}/expenses.pdf") as pdf:
        # plt.plot(name, amount)
        plt.bar(categories, amount)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel("Despesas", fontsize=12)

        plt.title(title)

        pdf.savefig()
        plt.close()
