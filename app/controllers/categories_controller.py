from http import HTTPStatus

from app.models.categories_model import CategoryModel
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy import BaseQuery
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound

TRUSTED_CATEGORY_KEYS = ['name', 'description']


@jwt_required()
def create_category():

    data = request.get_json()

    # try:
    #     verify_required_keys(data, TRUSTED_CATEGORY_KEYS)
    # except KeyError as err:
    #     return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    try:
        new_category = CategoryModel(**data)
    except TypeError as err:
        return jsonify({"err": err.description}), HTTPStatus.BAD_REQUEST

    session: Session = current_app.db.session()

    try:
        session.add(new_category)
        session.commit()
    except IntegrityError:
        return {"msg": "Category already exists!"}, HTTPStatus.CONFLICT

    return jsonify(new_category), HTTPStatus.CREATED


@jwt_required()
def update_category(category_id: int):

    session: Session = current_app.db.session
    base_query: BaseQuery = session.query(CategoryModel)

    try:
        category = base_query.get_or_404(category_id, description="Category not found!")
    except NotFound as error:
        return {"msg": error.description}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    # try:
    #     verify_allowed_keys(data, TRUSTED_CATEGORY_KEYS)
    # except KeyError as err:
    #     return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    for key, value in data.items():
        setattr(category, key, value)

    session.commit()

    return jsonify(category), HTTPStatus.OK

@jwt_required()
def list_categories():

    query = CategoryModel.query.all()

    return jsonify(query), HTTPStatus.OK
