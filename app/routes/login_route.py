from flask import Blueprint
from app.controllers.users_controller import login


bp = Blueprint("login_bp", __name__, url_prefix="/login")


bp.post("")(login)
