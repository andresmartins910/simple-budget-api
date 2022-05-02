from http import HTTPStatus
from turtle import title

from app.models.categories_model import CategoryModel
from app.services import verify_allowed_keys, verify_required_keys
from flask import current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from werkzeug.exceptions import NotFound

TRUSTED_CATEGORY_KEYS = ['name', 'description']
ALLOWED_CATEGORY_KEYS = ['name', 'description']


@jwt_required()
def create_category():

    current_user = get_jwt_identity()

    data = request.get_json()

    try:
        verify_required_keys(data, TRUSTED_CATEGORY_KEYS)
        verify_allowed_keys(data, ALLOWED_CATEGORY_KEYS)
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    data['created_by'] = str(current_user['id'])

    session: Session = current_app.db.session
    base_query: BaseQuery = session.query(CategoryModel)
    category_in_user_found = (base_query.filter(or_(CategoryModel.created_by == 'ADM',
                                                   CategoryModel.created_by == str(current_user['id'])))
                                        .filter(CategoryModel.name == data['name'].title())
                                        .one_or_none()
    )

    if category_in_user_found:
        return {"msg": "Category already exists!"}, HTTPStatus.CONFLICT

    try:
        new_category = CategoryModel(**data)
    except TypeError as err:
        return jsonify({"err": err.description}), HTTPStatus.BAD_REQUEST

    session: Session = current_app.db.session()

    session.add(new_category)
    session.commit()

    return jsonify(new_category), HTTPStatus.CREATED


@jwt_required()
def update_category(category_id: int):

    current_user = get_jwt_identity()

    session: Session = current_app.db.session
    base_query: BaseQuery = session.query(CategoryModel)

    try:
        category = base_query.get_or_404(category_id, description="Category not found!")
    except NotFound as error:
        return {"msg": error.description}, HTTPStatus.NOT_FOUND

    data = request.get_json()

    try:
        verify_required_keys(data, TRUSTED_CATEGORY_KEYS)
        verify_allowed_keys(data, ALLOWED_CATEGORY_KEYS)
    except KeyError as err:
        return jsonify(err.args[0]), HTTPStatus.BAD_REQUEST

    session: Session = current_app.db.session
    base_query: BaseQuery = session.query(CategoryModel)
    category_in_user_found = (base_query.filter(or_(CategoryModel.created_by == 'ADM',
                                                   CategoryModel.created_by == str(current_user['id'])))
                                        .filter(CategoryModel.name == data['name'].title())
                                        .one_or_none()
    )

    if category_in_user_found:
        return {"msg": "Category already exists!"}, HTTPStatus.CONFLICT

    for key, value in data.items():
        setattr(category, key, value)

    session.commit()

    return jsonify(category), HTTPStatus.OK


@jwt_required()
def list_categories():

    current_user = get_jwt_identity()

    session: Session = current_app.db.session

    categories: BaseQuery = (session.query(CategoryModel)
                                    .filter(or_(CategoryModel.created_by == 'ADM',
                                                CategoryModel.created_by == str(current_user['id'])))
                                    .all()
    )

    return jsonify(categories), HTTPStatus.OK


@jwt_required()
def delete_category(category_id: int):

    current_user = get_jwt_identity()

    session: Session = current_app.db.session

    try:
        category: BaseQuery = (session.query(CategoryModel)
                                    .filter(or_(CategoryModel.created_by == 'ADM',
                                                CategoryModel.created_by == str(current_user['id'])))
                                    .filter_by(id=category_id)
                                    .one()
    )
    except NotFound as err:
        return {"msg": "Category not found!"}, HTTPStatus.NOT_FOUND

    session.delete(category)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
