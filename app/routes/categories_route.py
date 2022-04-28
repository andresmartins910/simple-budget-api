from flask import Blueprint

# import controllers

bp = Blueprint("categories_bp", __name__, url_prefix="/categories")

bp.get("")
bp.post("")
bp.patch("")
bp.delete("")