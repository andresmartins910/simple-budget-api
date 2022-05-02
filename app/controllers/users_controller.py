from flask import request, jsonify, current_app
from http import HTTPStatus
from app.models.users_model import UserModel
from sqlalchemy.exc import IntegrityError
from app.exceptions.users_exceptions import CPFExc, PhoneExc, BirthdateExc
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta


@jwt_required()
def user_info():
    user = get_jwt_identity()

    get_user = UserModel.query.get(user["id"])

    if(get_user):
        serialized = {
            "id": get_user.id,
            "name": get_user.name,
            "email": get_user.email,
            "phone": get_user.phone,
            "cpf": get_user.cpf,
            "birthdate": get_user.birthdate,
        }
        return jsonify(serialized), HTTPStatus.OK

    return {
        "error": "User doesn't exists"
    }, HTTPStatus.NOT_FOUND


def create_user():
    data = request.get_json()

    allowed_keys = ["name", "email", "phone", "cpf", "birthdate", "password"]
    nullable_keys = ["cpf", "birthdate"]
    denied_nullable_keys = []
    wrong_keys = []
    missing_keys = []


    for i in nullable_keys:
        if(i not in data.keys()):
            denied_nullable_keys.append(i)


    for i in data.keys():
        if(i not in allowed_keys):
            wrong_keys.append(i)


    for i in allowed_keys:
        if(i not in data.keys() and i not in denied_nullable_keys):
            missing_keys.append(i)


    if(wrong_keys):
        return {
            "allowed_keys": allowed_keys,
            "wrong_keys": wrong_keys
        }, HTTPStatus.BAD_REQUEST

    if(missing_keys):
        return {
            "missing_keys": missing_keys
        }, HTTPStatus.BAD_REQUEST

    try:
        password_to_hash = data.pop("password")

        send_data = UserModel(**data)

        send_data.password = password_to_hash

        current_app.db.session.add(send_data)
        current_app.db.session.commit()

        serialized = {
            "name": send_data.name,
            "email": send_data.email,
            "phone": send_data.phone,
            "cpf": send_data.cpf,
            "birthdate": send_data.birthdate
        }

        return jsonify(serialized), HTTPStatus.CREATED

    except PhoneExc as e:
        return {
            "error": e.args[0]
        }, HTTPStatus.BAD_REQUEST

    except CPFExc as e:
        return {
            "error": e.args[0]
        }, HTTPStatus.BAD_REQUEST

    except BirthdateExc as e:
        return {
            "error": e.args[0]
        }, HTTPStatus.BAD_REQUEST

    except BirthdateExc as e:
        return {
            "error": e.args[0]
        }, 400

    except IntegrityError as e:
        if("email" in e.args[0]):
            return {"error": "EMAIL already exists"}, HTTPStatus.BAD_REQUEST
        if("password_hash" in e.args[0]):
            return {"error": "PASSWORD already exists"}, HTTPStatus.BAD_REQUEST
        if("phone" in e.args[0]):
            return {"error": "PHONE already exists"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def update_user():
    data = request.get_json()

    user = get_jwt_identity()

    allowed_keys = ["name", "email", "phone", "cpf", "birthdate", "password"]
    wrong_keys = []

    if(len(data) == 0):
        return {
            "allowed_keys": allowed_keys
        }, HTTPStatus.BAD_REQUEST


    for i in data.keys():
        if(i not in allowed_keys):
            wrong_keys.append(i)


    if(wrong_keys):
        return {
            "wrong_keys": wrong_keys
        }, HTTPStatus.BAD_REQUEST


    try:
        get_user = UserModel.query.filter_by(id = user["id"]).first()

        if(get_user == None):
            return {
                "error": "User not found"
            }, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(get_user, key, value)

        current_app.db.session.add(get_user)
        current_app.db.session.commit()

        serialized = {
            "id": get_user.id,
            "name": get_user.name,
            "email": get_user.email,
            "phone": get_user.phone,
            "cpf": get_user.cpf,
            "birthdate": get_user.birthdate
        }

        return jsonify(serialized), HTTPStatus.OK

    except CPFExc as e:
        return {
            "error": e.args[0]
        }, HTTPStatus.BAD_REQUEST

    except PhoneExc as e:
        return {
            "error": e.args[0]
        }, HTTPStatus.BAD_REQUEST

    except BirthdateExc as e:
        return {
            "error": e.args[0]
        }, HTTPStatus.BAD_REQUEST


@jwt_required()
def delete_user():
    try:
        user = get_jwt_identity()

        if(user):
            serialized_user = UserModel.query.get(user["id"])

            current_app.db.session.delete(serialized_user)
            current_app.db.session.commit()

            return "", HTTPStatus.OK

        return {
            "error": "Server Error"
        }, HTTPStatus.INTERNAL_SERVER_ERROR

    except:
        return {
            "error": "User doesn't exists"
        }, HTTPStatus.NOT_FOUND


def login():
    data = request.get_json()

    allowed_keys = ["email", "password"]
    missing_keys = []
    wrong_keys = []

    for i in allowed_keys:
        if(i not in data.keys()):
            missing_keys.append(i)


    for i in data.keys():
        if(i not in allowed_keys):
            wrong_keys.append(i)


    if(missing_keys):
        return {
            "allowed_keys": allowed_keys,
            "missing_keys": missing_keys
        }, HTTPStatus.BAD_REQUEST


    if(wrong_keys):
        return {
            "wrong_keys": wrong_keys
        }, HTTPStatus.BAD_REQUEST

    user = UserModel.query.filter_by(email = data["email"]).first()

    try:
        if(user and user.verify_password(data["password"])):
            token = create_access_token(user, expires_delta=timedelta(hours=24))

            return {
                "access_token": token
            }, HTTPStatus.OK

        return {
            "error": "email or password doesn't matches"
        }, HTTPStatus.NOT_FOUND

    except:
        return {
            "error": "Error"
        }, HTTPStatus.BAD_REQUEST
