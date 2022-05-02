from flask import Blueprint

from app.controllers import categories_controller

bp = Blueprint("categories_bp", __name__, url_prefix="/categories")

bp.get("")(categories_controller.list_categories)
bp.post("")(categories_controller.create_category)
bp.patch("/<int:category_id>")(categories_controller.update_category)
bp.delete("/<int:category_id>")(categories_controller.delete_category)
