from flask import Blueprint
from app.controllers.users_controller import user_info, create_user, update_user, delete_user


bp = Blueprint("register_bp", __name__, url_prefix="/register")

bp.get("")(user_info)
bp.post("")(create_user)
bp.patch("")(update_user)
bp.delete("")(delete_user)