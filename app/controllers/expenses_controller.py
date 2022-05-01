from http import HTTPStatus
from flask import request, jsonify
from ipdb import set_trace
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query
from datetime import datetime as dt
from app.configs.database import db
from app.models.budgets_model import BudgetModel
from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel

def all_expenses():
    session: Session = db.session
    # TODO: try/except
    expenses = session.query(ExpenseModel).all()
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
	        # "user_id": expense.category_id
        }
        list_expense.append(new_expense)
    return "", 200


@jwt_required()
def add_expense():
    data = request.get_json() # name, amount, description?
    session: Session = db.session
    try:
        data['created_at'] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        category_request = data.pop('category')
        category: CategoryModel = session.query(CategoryModel).filter(CategoryModel.name == category_request).first()
        data['category_id'] = category.id
        budget: BudgetModel = session.query(BudgetModel).get(data['budget_id'])
        expense = ExpenseModel(**data)
        expense.budget = budget
        expense.category = category
    except (Exception):
        raise TypeError

    try:
        session.add(expense)
        session.commit()
    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT

    return {"msg": "deu certo"}, HTTPStatus.CREATED


@jwt_required()
def get_expense(expense_id):
    session: Session = db.session
    # TODO: pegar o budget pelo ID, e atualizar pegar as expenses relacionadas a esse budget

    return "", 200


@jwt_required()
def update_expense(expense_id):
    data = request.get_json()
    session: Session = db.session
    expense =  session.query(ExpenseModel).get(expense_id)
    if not expense:
        return {"error": "expense not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(expense, key, value)

    # TODO: try/except
    session.commit()

    return "", 200


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


