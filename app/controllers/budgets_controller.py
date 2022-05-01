from datetime import datetime
from http import HTTPStatus

from app.configs.database import db
from app.models import BudgetModel
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


@jwt_required()
def get_budgets():

    current_user = get_jwt_identity()

    session: Session = db.session()

    budgets:BaseQuery = session.query(BudgetModel).filter_by(user_id=current_user['id']).all()

    return jsonify(budgets), HTTPStatus.OK


@jwt_required()
def create_budget():

    session: Session = db.session()

    data = request.get_json()

    current_user = get_jwt_identity()

    try:
        data['month_year'] = datetime.strptime(data['month_year'], "%m/%Y").strftime("%m/%Y")

        data['user_id'] = current_user['id']

        budget_found: BaseQuery = (session.query(BudgetModel)
                                        .filter(BudgetModel.month_year == data['month_year'])
                                        .filter(BudgetModel.user_id == data['user_id'])
                                        .one_or_none()
        )

        if budget_found:
            return {
                "error": "Budget already exists",
                "description": "You can only have one budget per month, each year"
            }, HTTPStatus.CONFLICT

        budget = BudgetModel(**data)

        session.add(budget)
        session.commit()

        return jsonify(budget), HTTPStatus.CREATED

    except ValueError:
        return jsonify({"error": "Field 'month_year' must be format: mm/YYYY"}), HTTPStatus.BAD_REQUEST

    # TORNOU-SE DESNECESSÁRIO
    # except IntegrityError as e:
    #     if type(e.orig) == UniqueViolation:

    #         return {
    #             "error": "Budget already exists",
    #             "description": "You can only have one budget per month, each year"
    #         }, HTTPStatus.CONFLICT
    #     elif type(e.orig) == ForeignKeyViolation:

    #         return {
    #             "error": "User don't exists",
    #             "description": "You can only register budget for users present in the database."
    #         }, HTTPStatus.CONFLICT

@jwt_required()
def update_budget(budget_id):

    current_user = get_jwt_identity()

    session: Session = db.session
    base_query: BaseQuery = session.query(BudgetModel)

    try:
        budget = (base_query
                        .filter_by(user_id=current_user['id'])
                        .filter_by(id=budget_id)
                        .one()
    )
    except NoResultFound:
        return {"msg": "Budget not found"}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    try:
        data['month_year'] = datetime.strptime(data['month_year'], "%m/%Y").strftime("%m/%Y")

        data['user_id'] = current_user['id']

        budget_found: BaseQuery = (session.query(BudgetModel)
                                        .filter(BudgetModel.month_year == data['month_year'])
                                        .filter(BudgetModel.user_id == data['user_id'])
                                        .one_or_none()
        )

        if budget_found:
            return {
                "error": "Budget already exists",
                "description": "You can only have one budget per month, each year"
            }, HTTPStatus.CONFLICT

        for key, value in data.items():
            setattr(budget, key, value)

        session.commit()

        budget_return = {
            "id": budget.id,
            "month_year": budget.month_year,
            "max_value": budget.max_value,
            # OPÇÃO DE RETORNO ABAIXO
            # "user": budget.user.name,
            # "expenses": [expense.name for expense in budget.expenses]
        }

        return jsonify(budget_return), HTTPStatus.OK

    except ValueError:
        return jsonify({"error": "Field 'month_year' must be format: mm/YYYY"}), HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_budget(budget_id):

    current_user = get_jwt_identity()

    session: Session = db.session
    base_query: BaseQuery = session.query(BudgetModel)

    try:
        budget = (base_query
                        .filter_by(user_id=current_user['id'])
                        .filter_by(id=budget_id)
                        .one()
    )
    except NoResultFound:
        return {"msg": "Budget not found"}, HTTPStatus.NOT_FOUND

    session.delete(budget)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
