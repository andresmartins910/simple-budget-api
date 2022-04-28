from flask import Blueprint

# import controllers

bp = Blueprint("budgets_bp", __name__, url_prefix="/budgets")

bp.get("")
bp.post("")
bp.patch("")
bp.delete("")
