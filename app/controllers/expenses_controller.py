from http import HTTPStatus
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError
from sqlalchemy.orm import Session, Query
from datetime import datetime as dt
from app.configs.database import db
from app.exceptions.expenses_exceptions import ValuesTypeError
from app.models.budgets_model import BudgetModel
from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.models.users_model import UserModel
from app.services import verify_allowed_keys, verify_required_keys
from app.services.expense_service import verify_update_type, verify_value_types


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
                "budget_month_year": budget.month_year,
                "budget_id": budget.id
            }
            list_expense.append(new_expense)

    return jsonify(list_expense), HTTPStatus.OK


@jwt_required()
def add_expense():
    data = request.get_json()
    trusted_expense_keys = ['name','amount','category_id','budget_id']
    allowed_keys = ['name','amount', 'description','category_id','budget_id']
    try:
        verify_required_keys(data, trusted_expense_keys)
        verify_allowed_keys(data, allowed_keys)
        verify_value_types(data)
    except KeyError as e:
        return jsonify(e.args), HTTPStatus.BAD_REQUEST
    except ValuesTypeError as e:
        return jsonify(e.args), HTTPStatus.BAD_REQUEST
    
    session: Session = db.session
    
    budget_found = session.query(BudgetModel).filter(BudgetModel.id == data['budget_id']).one_or_none()
    if not budget_found:
        return {
            "error": "Budget not exist"
        }, HTTPStatus.NOT_FOUND
    
    category_found = session.query(BudgetModel).filter(BudgetModel.id == data['category_id']).one_or_none()
    if not category_found:
        return {
            "error": "Category not exist"
        }, HTTPStatus.NOT_FOUND

    expense_name = [expense.name for expense in budget_found.expenses if expense.name not in budget_found.expenses]
    if data['name'] in expense_name:
        return {
            "error": "Expense already exists",
            "description": "You can only have one expense per budget"
        }, HTTPStatus.CONFLICT

    try:
        data['created_at'] = dt.now()
        expense = ExpenseModel(**data)
        session.add(expense)
        session.commit()
    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT

    serialized = {
            "id": expense.id,
	        "name": expense.name,
	        "description": expense.description,
	        "amount": expense.amount,
            "created_at": expense.created_at,
            "budget_id": expense.budget_id,
	        "category": expense.category.name,
            "budget": expense.budget.month_year
        }

    return jsonify(serialized), HTTPStatus.CREATED


@jwt_required()
def get_expense(expense_id):
    session: Session = db.session
    expense = session.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()

    return jsonify(expense), HTTPStatus.OK


@jwt_required()
def budget_expenses(budget_id):
    session: Session = db.session
    budget = session.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if not budget:
        return {"error": "budget not found"}, HTTPStatus.NOT_FOUND
    expenses = budget.expenses
    if expenses == []:
        return {"msg": "whitout expenses in this budget please create one"}, HTTPStatus.OK
    
    return jsonify(expenses), 200


@jwt_required()
def update_expense(expense_id):
    data = request.get_json()
    current_user = get_jwt_identity()
    trusted_update_keys = ['name','description','amount']
    try:
        verify_allowed_keys(data, trusted_update_keys)
        verify_update_type(data)

    except KeyError as e:
        return jsonify(e.args), HTTPStatus.BAD_REQUEST
    except ValuesTypeError as e:
        return jsonify(e.args), HTTPStatus.BAD_REQUEST

    session: Session = db.session
    expense =  session.query(ExpenseModel).get(expense_id)

    if not expense:
        return {"error": "expense not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(expense, key, value)

    try:
        session.commit()
    except DataError as err:
        if type(err.orig).__name__ == "InvalidTextRepresentation":
            return {"error": "amount must be of type integer"}

    return {
        "id": expense.id,
        "name": expense.name,
        "description": expense.description,
        "amount": expense.amount,
        "created_at": expense.created_at,
        "category":  expense.category.name,
        "budget_id": expense.budget_id,
        "user_id": current_user['id']
    }, HTTPStatus.OK


@jwt_required()
def del_expense(expense_id):
    session: Session = db.session
    expense =  session.query(ExpenseModel).get(expense_id)
    if not expense:
        return {"error": "expense not found"}, HTTPStatus.NOT_FOUND

    session.delete(expense)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
