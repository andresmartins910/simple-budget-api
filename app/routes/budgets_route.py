from flask import Blueprint
from app.controllers import budgets_controller

bp = Blueprint("budgets_bp", __name__, url_prefix="/budgets")

bp.get("")(budgets_controller.get_budgets)
bp.post("")(budgets_controller.create_budget)
bp.patch("/<int:id>")(budgets_controller.update_budget)
bp.delete("/<int:id>")(budgets_controller.delete_budget)
