from flask import Blueprint

from app.controllers import expenses_controller

bp = Blueprint("expenses_bp", __name__, url_prefix="/expenses")

# bp.get("<expense_id>")(expenses_controller.get_expense)
bp.get("")(expenses_controller.all_expenses)
bp.get("<int:budget_id>")(expenses_controller.budget_expenses)
bp.post("")(expenses_controller.add_expense)
bp.patch("<int:expense_id>")(expenses_controller.update_expense)
bp.delete("<int:expense_id>")(expenses_controller.del_expense)
