from datetime import datetime as dt
from http import HTTPStatus

from app.configs.database import db
# from app.services.expense_service import verify_update_type, verify_value_types
from app.exceptions import InvalidDataTypeError
from app.exceptions.expenses_exceptions import ValuesTypeError
from app.models.budgets_model import BudgetModel
from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.models.users_model import UserModel
from app.services import verify_allowed_keys, verify_required_keys
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import DataError, IntegrityError, NoResultFound
from sqlalchemy.orm import Query, Session


@jwt_required()
def all_expenses():

    session: Session = db.session

    current_user = get_jwt_identity()

    user = (session.query(UserModel).filter_by(id=current_user['id']).one())
    budgets = user.budgets

    list_expense = []
    for budget in budgets:
        expenses = budget.expenses
        for expense in expenses:
            new_expense = {
                "id": expense.id,
                "name": expense.name,
                "description": expense.description,
                "amount": expense.amount,
                "created_at": expense.created_at,
                "category": expense.category.name,
                "budget": budget.month_year
            }
            list_expense.append(new_expense)

    return jsonify(list_expense), HTTPStatus.OK


@jwt_required()
def add_expense():

    data = request.get_json()

    TRUSTED_TASK_KEYS = ['name','amount','category_id','budget_id']
    ALLOWED_TASK_KEYS = ['name','amount', 'description','category_id','budget_id']

    try:
        verify_required_keys(data, TRUSTED_TASK_KEYS)
        verify_allowed_keys(data, ALLOWED_TASK_KEYS)
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    session: Session = db.session

    budget_found = session.query(BudgetModel).filter(BudgetModel.id == data['budget_id']).one_or_none()
    if not budget_found:
        return {
            "error": "Budget not exist."
        }, HTTPStatus.BAD_REQUEST

    category_found = session.query(CategoryModel).filter(CategoryModel.id == data['category_id']).one_or_none()
    if not category_found:
        return {
            "error": "Category not exist."
        }, HTTPStatus.BAD_REQUEST

    try:
        data['created_at'] = dt.now()

        expense = ExpenseModel(**data)

        expense_found: BaseQuery = (session.query(ExpenseModel)
                                        .filter(ExpenseModel.name == data['name'].capitalize())
                                        .filter(ExpenseModel.budget_id == data['budget_id'])
                                        .one_or_none()
        )

        if expense_found:
            return {
                "error": "Expense already exists",
                "description": "You can't have two expenses with the same names in your budget."
            }, HTTPStatus.CONFLICT

        session.add(expense)
        session.commit()

    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT

    except InvalidDataTypeError as err:
        return jsonify({"err": err.description}), HTTPStatus.BAD_REQUEST

    serialized = {
            "id": expense.id,
	        "name": expense.name,
	        "description": expense.description,
	        "amount": expense.amount,
            "created_at": expense.created_at,
	        "category": expense.category.name,
            "budget": expense.budget.month_year
        }

    return jsonify(serialized), HTTPStatus.CREATED


@jwt_required()
def get_expense(expense_id):

    current_user = get_jwt_identity()

    session: Session = db.session

    expense = session.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()

    if not expense or expense.budget.user_id != current_user['id']:
        return {"error": "Expense not found!"}, HTTPStatus.NOT_FOUND

    serialized = {
            "id": expense.id,
	        "name": expense.name,
	        "description": expense.description,
	        "amount": expense.amount,
            "created_at": expense.created_at,
	        "category": expense.category.name,
            "budget": expense.budget.month_year
        }

    return jsonify(serialized), HTTPStatus.OK


@jwt_required()
def budget_expenses(budget_id):
    session: Session = db.session
    budget = session.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if not budget:
        return {"error": "Budget not found"}, HTTPStatus.NOT_FOUND
    expenses = budget.expenses
    if expenses == []:
        return {"msg": "whitout expenses in this budget please create one"}, HTTPStatus.OK

    return jsonify(expenses), HTTPStatus.OK


@jwt_required()
def update_expense(expense_id):

    data = request.get_json()

    current_user = get_jwt_identity()

    ALLOWED_TASK_KEYS = ['name', 'amount', 'description', 'category_id']

    try:
        verify_allowed_keys(data, ALLOWED_TASK_KEYS)
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    # trusted_update_keys = ['name','description','amount']
    # try:
    #     verify_allowed_keys(data, trusted_update_keys)
    #     verify_update_type(data)

    # except KeyError as e:
    #     return jsonify(e.args), HTTPStatus.BAD_REQUEST
    # except ValuesTypeError as e:
    #     return jsonify(e.args), HTTPStatus.BAD_REQUEST

    session: Session = db.session
    expense = session.query(ExpenseModel).get(expense_id)

    if not expense or expense.budget.user_id != current_user['id']:
        return {"error": "Expense not found!"}, HTTPStatus.NOT_FOUND

    if 'name' in data.items():
        expense_found: BaseQuery = (session.query(ExpenseModel)
                                        .filter(ExpenseModel.name == data['name'].capitalize())
                                        .filter(ExpenseModel.budget_id == expense.budget_id)
                                        .one_or_none()
        )

        if expense_found:
            return {
                "error": "Expense already exists",
                "description": "You can't have two expenses with the same names in your budget."
            }, HTTPStatus.CONFLICT

    for key, value in data.items():
        setattr(expense, key, value)

    session.commit()

    # try:
    # except DataError as err:
    #     if type(err.orig).__name__ == "InvalidTextRepresentation":
    #         return {"error": "amount must be of type integer"}

    serialized = {
        "id": expense.id,
        "name": expense.name,
        "description": expense.description,
        "amount": expense.amount,
        "created_at": expense.created_at,
        "category":  expense.category.name,
        "budget": expense.budget.month_year
    }

    return jsonify(serialized), HTTPStatus.OK


@jwt_required()
def del_expense(expense_id):

    current_user = get_jwt_identity()

    session: Session = db.session
    expense =  session.query(ExpenseModel).get(expense_id)

    if not expense or expense.budget.user_id != current_user['id']:
        return {"error": "Expense not found!"}, HTTPStatus.NOT_FOUND

    session.delete(expense)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
