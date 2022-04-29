from http import HTTPStatus
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Query
from datetime import datetime as dt
from app.configs.database import db
from app.models.expenses_model import ExpenseModel


def add_expense():
    data = request.get_json()
    session: Session = db.session
    try:
        # TODO: adicionar ao data p create_at
        # data['create_at'] = dt.now()
        expense = ExpenseModel(**data)
    except (Exception):
        raise TypeError

    try:
        session.add(expense)
        session.commit()
    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT
    
    return "", HTTPStatus.CREATED


def get_expense(id):
    session: Session = db.session
    # TODO: pegar o budget pelo ID, e atualizar pegar as expenses relacionadas a esse budget

    return "", 200


def update_expense(id):
    data = request.get_json()
    session: Session = db.session
    expense =  session.query(ExpenseModel).get(id)
    if not expense:
        return {"error": "categorie not found"}, HTTPStatus.NOT_FOUND
    
    for key, value in data.items():
        setattr(expense, key, value)
    
    # TODO: try/except
    session.commit()

    return "", 200


def del_expense(id):
    session: Session = db.session
    expense =  session.query(ExpenseModel).get(id)
    if not expense:
        return {"error": "categorie not found"}, HTTPStatus.NOT_FOUND
    
    # TODO: try/except
    session.delete(expense)
    session.commit()

    return "", HTTPStatus.NO_CONTENT


