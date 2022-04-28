from flask import Blueprint

# import controllers

bp = Blueprint("register_bp", __name__, url_prefix="/register")

bp.get("")
bp.post("")
bp.patch("")
bp.delete("")