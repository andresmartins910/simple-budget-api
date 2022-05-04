from http import HTTPStatus
from flask import current_app, jsonify, request
from app.configs.database import db
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, or_
from flask_jwt_extended import get_jwt_identity, jwt_required
from datetime import datetime as dt


from app.models.users_model import UserModel
from app.models.budgets_model import BudgetModel
from app.models.expenses_model import ExpenseModel
from app.models.categories_model import CategoryModel


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

        #  EXEMPLO DE QUERY
        # registers: Query = (
        #     registers
        #     .select_from(table1)
        #     .join(table2)
        #     .join(table3)
        #     .filter(func.lower(table1.name) == value.lower())
        #     .filter(or_(func.lower(table2.job) == job.lower(),
        #                 func.lower(table2.job) == value2.lower())
        #             )
        #     .filter_by(age=value3)
        #     .all()
        # )

        # /xls ( Relatório completo do usuário - Todos os Budgets e expenses do cadastro )
        ...

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

        # /xls?category_id=1 ( Query param especificando a categoria do expenses no relatório )

        ...

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
    ...