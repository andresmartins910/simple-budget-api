from flask import jsonify, request

from app.models import BudgetModel

from app.configs.database import db

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from psycopg2.errors import UniqueViolation


def get_budgets():
    return "", 200

def create_budget():
    session: Session = db.session()
    data = request.get_json()

    try:
        data["month"] = data["month"].title()
        budget = BudgetModel(**data)

        session.add(budget)
        session.commit()

        return jsonify(budget), 201

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"error": "Budget already exists"}, 409

def update_budget(id):
    return "", 200

def delete_budget(id):
    return "", 200