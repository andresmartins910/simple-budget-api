from http import HTTPStatus
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session, Query
from datetime import datetime as dt
from app.configs.database import db
from app.models.budgets_model import BudgetModel
from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.services import verify_required_keys


@jwt_required()
def all_expenses():
    session: Session = db.session
    current_user = get_jwt_identity()

    try:
        expenses = (session.query(ExpenseModel)
                        .filter_by(user_id=current_user['id'])
                        .all()
    )
    except NoResultFound:
        return {"msg": "Budget not found"}, HTTPStatus.NOT_FOUND
    if expenses == []:
        return {"message": "whitout content"}, HTTPStatus.NO_CONTENT
    list_expense = []
    for expense in expenses:
        new_expense = {
            "id": expense.id,
	        "name": expense.name,
	        "description": expense.description,
	        "amount": expense.amount,
            "created_at": expense.create_at,
            "budget_id": expense.budget_id,
	        "user_id": current_user['id']
        }
        list_expense.append(new_expense)
    return "", 200


@jwt_required()
def add_expense():
    data = request.get_json()
    trusted_expense_keys = ['name','description','amount','category_id','budget_id']
    try:
        verify_required_keys(data, trusted_expense_keys)
    
    except KeyError as e:
        return jsonify(e.args), HTTPStatus.BAD_REQUEST

    session: Session = db.session
    try:
        data['created_at'] = dt.now()
        expense = ExpenseModel(**data)
        session.add(expense)
        session.commit()
    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT
    # except (Exception):
        # raise TypeError

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
def update_expense(expense_id):
    data = request.get_json()
    trusted_update_keys = ['name','description','amount']
    try:
        verify_required_keys(data, trusted_update_keys)

    except KeyError as e:
        return jsonify(e.args), HTTPStatus.BAD_REQUEST

    session: Session = db.session
    expense =  session.query(ExpenseModel).get(expense_id)

    if not expense:
        return {"error": "expense not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(expense, key, value)

    # TODO: try/except
    session.commit()

    return {
        "id": expense.id,
        "name": expense.name,
        "description": expense.description,
        "amount": expense.amount,
        "created_at": expense.created_at,
        "category_id": expense.category_id,
        "budget_id": expense.budget_id
    }, HTTPStatus.OK


@jwt_required()
def del_expense(expense_id):
    session: Session = db.session
    expense =  session.query(ExpenseModel).get(expense_id)
    if not expense:
        return {"error": "expense not found"}, HTTPStatus.NOT_FOUND

    # TODO: try/except
    session.delete(expense)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
