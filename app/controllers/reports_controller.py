from http import HTTPStatus
from flask import current_app, jsonify, request
from app.configs.database import db
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, or_
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime as dt
import json


from app.models.users_model import UserModel
from app.models.budgets_model import BudgetModel
from app.models.expenses_model import ExpenseModel
from app.models.categories_model import CategoryModel
from app.services.pdf_service import rel_pdf_time_year


from ..services import send_mail, download_file


def download():

    file_name = ""

    try:
        downloaded_file = download_file(file_name)
    except FileNotFoundError as e_not_found:
        return e_not_found.args[0], HTTPStatus.NOT_FOUND

    return downloaded_file, HTTPStatus.OK


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

            #  teste
        # to_test = json.dumps(expenses)

        # test_pandas(to_test)
            # teste
        data_return = {
            "user": current_user['name'],
            "year": year,
            "expenses": expenses
        }

        rel_pdf_time_year()

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

        return jsonify(data_return), HTTPStatus.OK

    elif year and not category_id and not initial_date and not final_date:

        try:
            year_ok = dt.strptime(year, "%Y")
        except:
            return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

        registers: Query = (
            expenses_registers
            .select_from(ExpenseModel)
            .join(BudgetModel)
            .join(UserModel)
            .filter(UserModel.id == current_user['id'])
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
            "budgets": sorted(budgets, key=lambda budget: budget['month_year'])
        }

        return jsonify(data_return), HTTPStatus.OK

    elif category_id and not year and not initial_date and not final_date:

        category = session.query(CategoryModel).get(category_id)

        if not category:
            return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

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

        return jsonify(data_return), HTTPStatus.OK

    elif category_id and year and not initial_date and not final_date:

        session: Session = db.session

        category = session.query(CategoryModel).get(category_id)

        if not category:
            return {"error": "category not found."}, HTTPStatus.BAD_REQUEST

        try:
            year_ok = dt.strptime(year, "%Y")
        except:
            return {"error": "year must be format 'YYYY'."}, HTTPStatus.BAD_REQUEST

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

        return jsonify(data_return), HTTPStatus.OK

    elif initial_date and final_date and not year and not category_id:

        try:
            initial_date_ok = dt.strptime(initial_date, "%d/%m/%Y")
            final_date_ok = dt.strptime(final_date, "%d/%m/%Y")
        except:
            return {"error": "start and end dates must be format 'dd/mm/YYYY'."}, HTTPStatus.BAD_REQUEST

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

        return jsonify(data_return), HTTPStatus.OK

    else:
        return jsonify({"error": "This request is not allowed."}), HTTPStatus.BAD_REQUEST


@jwt_required()
def report_with_filter_by_budget_to_pdf(budget_id):

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
        "expenses": sorted(expenses, key=lambda expense: expense['created_at'])
    }

    return jsonify(data_return), HTTPStatus.OK

