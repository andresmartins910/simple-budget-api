from datetime import datetime as dt
from http import HTTPStatus

from app.configs.database import db
from app.models.budgets_model import BudgetModel
from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.models.users_model import UserModel
from app.services.json_to_excel import json_to_excel
from app.services.pdf_service import rel_all_budget, rel_pdf_time_year
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import Query, Session

from ..services import download_file, send_mail
from ..services.pdf_service import (create_pdf, normalize_amount,
                                    rel_all_budget, rel_by_category,
                                    rel_by_category_year, rel_pdf_time_month,
                                    rel_pdf_time_period, rel_pdf_time_year)

# FUNÇÕES DE DISTRIBUIDORAS

@jwt_required()
def download_xlsx():

    current_user = get_jwt_identity()
    attachments = ['report.xlsx']

    try:
        subject = report_with_filter()
        pdf_chart_to_mail()

        return download_file(attachments), HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def download_xlsx_budget_id(budget_id):

    session: Session = db.session()

    registers: BaseQuery = session.query(ExpenseModel)
    budget: BudgetModel = BudgetModel.query.filter_by(id=budget_id).first()

    if not budget:
        return {"error": "No data found in database"}

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

    subject = f'Mensal - {budget.month_year}'
    attachments = ['report.xlsx']

    try:
        report_with_filter_by_budget(registers, budget, current_user)

        return download_file(attachments), HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def download_pdf():

    current_user = get_jwt_identity()
    attachments = ['report.pdf', 'chart_report.pdf']

    try:
        subject = report_with_filters_to_pdf()
        pdf_chart_to_mail()

        return download_file(attachments), HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def download_pdf_budget_id(budget_id):

    session: Session = db.session()

    registers: BaseQuery = session.query(ExpenseModel)
    budget: BudgetModel = BudgetModel.query.filter_by(id=budget_id).first()

    if not budget:
        return {"error": "Budget not found!"}, HTTPStatus.NOT_FOUND

    current_user = get_jwt_identity()

    attachments = ['report.pdf', 'chart_report.pdf']

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

    try:
        report_with_filter_by_budget_to_pdf(registers, current_user, budget)
        pdf_chart_to_mail_by_budget_id(registers, budget)

        return download_file(attachments), HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def email_xlsx():

    current_user = get_jwt_identity()
    attachments = ['report.xlsx']

    try:
        subject = report_with_filter()
        pdf_chart_to_mail()

        send_mail(current_user['email'], subject, attachments)

        return "", HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def email_xlsx_budget_id(budget_id):

    session: Session = db.session()

    registers: BaseQuery = session.query(ExpenseModel)
    budget: BudgetModel = BudgetModel.query.filter_by(id=budget_id).first()

    if not budget:
        return {"error": "No data found in database"}

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

    subject = f'Mensal - {budget.month_year}'
    attachments = ['report.xlsx']

    try:
        report_with_filter_by_budget(registers, budget, current_user)

        send_mail(current_user['email'], subject, attachments)

        return "", HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def email_pdf():

    current_user = get_jwt_identity()
    attachments = ['report.pdf', 'chart_report.pdf']

    try:
        subject = report_with_filters_to_pdf()
        pdf_chart_to_mail()

        send_mail(current_user['email'], subject, attachments)

        return "", HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR


@jwt_required()
def email_pdf_budget_id(budget_id):

    session: Session = db.session()

    registers: BaseQuery = session.query(ExpenseModel)
    budget: BudgetModel = BudgetModel.query.filter_by(id=budget_id).first()

    if not budget:
        return {"error": "Budget not found!"}, HTTPStatus.NOT_FOUND

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

    subject = f'Mensal - {budget.month_year}'
    attachments = ['report.pdf', 'chart_report.pdf']

    try:
        report_with_filter_by_budget_to_pdf(registers, current_user, budget)
        pdf_chart_to_mail_by_budget_id(registers, budget)

        send_mail(current_user['email'], subject, attachments)

        return "", HTTPStatus.NO_CONTENT

    except:
        return {"Error": "Erro ao gerar os relatórios ou enviar email"}, HTTPStatus.INTERNAL_SERVER_ERROR






# FUNÇÕES DE QUERIES


def report_with_filter():

    session: Session = current_app.db.session

    registers: BaseQuery = session.query(ExpenseModel)

    current_user = get_jwt_identity()

    year = request.args.get("year", type=str)
    category_id = request.args.get("category_id", type=int)
    initial_date = request.args.get("initial_date", type=str)
    final_date = request.args.get("final_date", type=str)

    if not year and not category_id and not initial_date and not final_date:

        subject = f"Completo - {current_user['name']}"

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

        subject = f"Anual - {year}"

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

        subject = f"Por Categoria - {category.name}"

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

        subject = f"Por ano e categoria - {year}/{category.name}"

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

        subject = f"por Período - {initial_date}-{final_date}"

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

    json_to_excel(data_return)

    return subject


def report_with_filter_by_budget(registers, budget, current_user):

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

    json_to_excel(data_return)


def report_with_filters_to_pdf():

    session: Session = current_app.db.session

    budgets_registers: Query = session.query(BudgetModel)

    expenses_registers: Query = session.query(ExpenseModel)

    current_user = get_jwt_identity()

    year = request.args.get("year", type=str)
    category_id = request.args.get("category_id", type=int)
    initial_date = request.args.get("initial_date", type=str)
    final_date = request.args.get("final_date", type=str)

    if not year and not category_id and not initial_date and not final_date:

        subject = f"Completo - {current_user['name']}"

        registers: Query = (
            budgets_registers
            .select_from(BudgetModel)
            .join(ExpenseModel)
            .join(UserModel)
            .filter(UserModel.id == current_user['id'])
            .all()
        )

        budgets = []

        for budget in registers:

                new_budget = {
                    "month_year": dt.strptime(budget.month_year, "%m/%Y"),
                    "max_value": budget.max_value,
                    "expenses": []
                }

                for expense in budget.expenses:

                    new_expense = {
                        "name": expense.name,
                        "description": expense.description,
                        "amount": expense.amount,
                        "created_at": expense.created_at,
                        "category": expense.category.name
                    }

                    new_budget['expenses'].append(new_expense)

                budgets.append(new_budget)

        data_return = {
            "user": current_user["name"],
            "budgets": sorted(budgets, key=lambda budget: budget['month_year'])
        }

        rel_all_budget(data_return, current_user)

        return subject


    elif year and not category_id and not initial_date and not final_date:

        try:
            year_ok = dt.strptime(year, "%Y")
        except:
            return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

        subject = f"Anual - {year}"

        years_first_day = f"01/01/{year}"
        years_last_day = f"31/12/{year}"

        registers: Query = (
            budgets_registers
            .select_from(BudgetModel)
            .join(ExpenseModel)
            .join(UserModel)
            .filter(UserModel.id == current_user['id'])
            .all()
        )

        budgets = []

        for budget in registers:

            valid_year = dt.strptime(budget.month_year, "%m/%Y").strftime("%Y")

            if valid_year == year:

                new_budget = {
                                "month_year": dt.strptime(budget.month_year, "%m/%Y"),
                                "expenses": []
                            }

                for expense in budget.expenses:

                    new_expense = {
                                "name": expense.name,
                                "description": expense.description,
                                "amount": expense.amount,
                                "created_at": expense.created_at,
                                "category": expense.category.name
                            }

                    new_budget["expenses"].append(new_expense)

                budgets.append(new_budget)

        data_return = {
            "user": current_user['name'],
            "year": year,
            "budgets": sorted(budgets, key=lambda budget: budget['month_year'])
        }

        rel_pdf_time_year(data_return, current_user)

        return subject


    elif category_id and not year and not initial_date and not final_date:

        category = session.query(CategoryModel).get(category_id)

        if not category:
            return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

        subject = f"Por Categoria - {category.name}"

        registers: Query = (
            expenses_registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .join(CategoryModel)
            .filter(UserModel.id == current_user['id'])
            .filter(CategoryModel.id == category_id)
            .all()
        )

        budgets = []

        for expense in registers:

            new_budget = {
                "month_year": dt.strptime(expense.budget.month_year, "%m/%Y"),
                "expenses": []
            }

            for expense in registers:

                if dt.strptime(expense.budget.month_year, "%m/%Y") == new_budget['month_year']:

                    new_expense = {
                                "name": expense.name,
                                "description": expense.description,
                                "amount": expense.amount,
                                "created_at": expense.created_at,
                            }

                    new_budget["expenses"].append(new_expense)

            budgets.append(new_budget)

        data_return = {
            "user": current_user['name'],
            "category": category.name,
            "budgets": sorted(budgets, key=lambda budget: budget['month_year'])
        }

        rel_by_category(data_return, current_user)

        return subject


    elif category_id and year and not initial_date and not final_date:

        session: Session = db.session

        category = session.query(CategoryModel).get(category_id)

        if not category:
            return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

        try:
            year_ok = dt.strptime(year, "%Y")
        except:
            return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

        subject = f"Por ano e categoria - {year}/{category.name}"

        registers: Query = (
            expenses_registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .join(CategoryModel)
            .filter(UserModel.id == current_user['id'])
            .filter(CategoryModel.id == category_id)
            .all()
        )

        budgets = []

        for expense in registers:

            year_validate = dt.strptime(expense.budget.month_year, "%m/%Y").strftime("%Y")

            if year_validate == year:

                new_budget = {
                                "month_year": dt.strptime(expense.budget.month_year, "%m/%Y"),
                                "expenses": []
                            }

                for expense in registers:

                    if dt.strptime(expense.budget.month_year, "%m/%Y") == new_budget['month_year']:

                        new_expense = {
                                    "name": expense.name,
                                    "description": expense.description,
                                    "amount": expense.amount,
                                    "created_at": expense.created_at,
                                }

                        new_budget["expenses"].append(new_expense)

                budgets.append(new_budget)

        data_return = {
            "user": current_user['name'],
            "year": year,
            "category": category.name,
            "budgets": sorted(budgets, key=lambda budget: budget['month_year'])
        }

        rel_by_category_year(data_return, current_user)

        return subject


    elif initial_date and final_date and not year and not category_id:

        try:
            initial_date_ok = dt.strptime(initial_date, "%d/%m/%Y")
            final_date_ok = dt.strptime(final_date, "%d/%m/%Y")
        except:
            return {"error": "start and end dates must be format 'dd/mm/YYYY'."}, HTTPStatus.BAD_REQUEST

        subject = f"por Período - {initial_date}-{final_date}"

        registers: Query = (
            expenses_registers
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
            "expenses": sorted(expenses, key=lambda expense: expense['created_at'])
        }

        rel_pdf_time_period(data_return, current_user)

        return subject


    else:
        return jsonify({"error": "This request is not allowed."}), HTTPStatus.BAD_REQUEST


def report_with_filter_by_budget_to_pdf(registers, user, budget):

    expenses = []

    for expense in registers:
        new_expense = {
            "name": expense.name,
            "description": expense.description,
            "amount": expense.amount,
            "created_at": expense.created_at,
            "category":  expense.category.name,
        }

        expenses.append(new_expense)

    data_return = {
        "user": user['name'],
        "budget": budget.month_year,
        "expenses": sorted(expenses, key=lambda expense: expense['created_at'])
    }

    rel_pdf_time_month(data_return, user)


def pdf_chart_to_mail():

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
                create_pdf(name, amount, title, xlabel)

                return "", HTTPStatus.NO_CONTENT


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
                create_pdf(categories, new_amount, title, xlabel)

                return "", HTTPStatus.NO_CONTENT

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
                create_pdf(name, amount, title, xlabel)

                return "", HTTPStatus.NO_CONTENT

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

                create_pdf(categories, new_amount, title, xlabel)

                return "", HTTPStatus.NO_CONTENT

            return {
                "error": "Insufficient data or Wrong Data"
            }, HTTPStatus.BAD_REQUEST


        else:
            return {
                "error": "Wrong Arguments for Reports"
            }, HTTPStatus.BAD_REQUEST


def pdf_chart_to_mail_by_budget_id(registers, budget):

    amount = []

    total, categories = normalize_amount(registers)
    title = f"Despesas do Budget de {budget.month_year}"
    xlabel = "Categorias"

    for i in total:
        amount.append(i["amount"])

    if(len(categories) > 0 and len(amount) > 0):
        create_pdf(categories, amount, title, xlabel)

        return "", HTTPStatus.NO_CONTENT

    return {
        "error": "Insufficient data"
    }, HTTPStatus.BAD_REQUEST

