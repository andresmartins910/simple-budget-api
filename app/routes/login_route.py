from flask import Blueprint

# import controllers

bp = Blueprint("login_bp", __name__, url_prefix="/login")

bp.get("")
bp.post("")
bp.patch("")
bp.delete("")