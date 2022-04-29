from flask import Blueprint

from app.controllers import users_controller


bp = Blueprint("user_bp", __name__, url_prefix="/user")

bp.get("")(users_controller.user_info)
bp.post("")(users_controller.create_user)
bp.patch("")(users_controller.update_user)
bp.delete("")(users_controller.delete_user)