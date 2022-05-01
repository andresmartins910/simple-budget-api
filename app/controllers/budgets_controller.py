from datetime import datetime
from http import HTTPStatus

from app.configs.database import db
from app.models import BudgetModel
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy import BaseQuery
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from werkzeug.exceptions import NotFound


#@jwt_required()
def get_budgets():

    budgets = BudgetModel.query.all()

    return jsonify(budgets), HTTPStatus.OK

#@jwt_required()
def create_budget():
    session: Session = db.session()
    data = request.get_json()

    try:
        data['month_year'] = datetime.strptime(data['month_year'], "%m/%Y").strftime("%m/%Y")
        
        budget = BudgetModel(**data)

        session.add(budget)
        session.commit()
        
        return jsonify(budget), HTTPStatus.CREATED

    except ValueError:
        return jsonify({"error": "Field 'month_year' must be format: mm/YYYY"}), HTTPStatus.BAD_REQUEST

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            
            return {
                "error": "Budget already exists", 
                "description": "You can only have one budget per month, each year"
            }, HTTPStatus.CONFLICT

#@jwt_required()
def update_budget(budget_id):

    session: Session = db.session
    base_query: BaseQuery = session.query(BudgetModel)

    try:
        budget = base_query.get_or_404(budget_id, description="Budget not found!")
    except NotFound as err:
        return {"msg": err.description}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    for key, value in data.items():
        setattr(budget, key, value)

    session.commit()

    budget_return = {
        "id": budget.id,
        "month_year": budget.month_year,
        "max_value": budget.max_value,
        "user": budget.user.name,
        "expenses": [expense.name for expense in budget.expenses]
    }

    return jsonify(budget_return), HTTPStatus.OK

#@jwt_required()
def delete_budget(budget_id):

    session: Session = db.session
    base_query: BaseQuery = session.query(BudgetModel)

    try:
        budget = base_query.get_or_404(budget_id, description="Budget not found!")
    except NotFound as err:
        return {"msg": err.description}, HTTPStatus.NOT_FOUND

    session.delete(budget)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
