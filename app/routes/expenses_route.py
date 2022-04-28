from flask import Blueprint

# import controllers

bp = Blueprint("expenses_bp", __name__, url_prefix="/expenses")

bp.get("")
bp.post("")
bp.patch("")
bp.delete("")