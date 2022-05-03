from flask import Blueprint

# import controllers
from app.services import get_report_to_pdf

bp = Blueprint("reports_bp", __name__, url_prefix="/reports")

bp.get("/<int:type>")(get_report_to_pdf)

