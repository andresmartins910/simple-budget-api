from flask import Blueprint

from app.controllers.expenses_controller import add_expense, get_expense, update_expense, del_expense

bp = Blueprint("expenses_bp", __name__, url_prefix="/expenses")

bp.get("<id>")(get_expense)
bp.post("")(add_expense)
bp.patch("<id>")(update_expense)
bp.delete("<id>")(del_expense)
