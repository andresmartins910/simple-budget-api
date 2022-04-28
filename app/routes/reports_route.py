from flask import Blueprint

# import controllers

bp = Blueprint("reports_bp", __name__, url_prefix="/reports")

bp.get("")
bp.post("")
bp.patch("")
bp.delete("")
