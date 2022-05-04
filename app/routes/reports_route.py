from flask import Blueprint

from app.controllers import reports_controller

bp = Blueprint("reports_bp", __name__, url_prefix="/reports")

# ROTAS DE DOWNLOAD

# ROTAS COM RETORNO EM .xls

bp.get("/xls")(reports_controller.report_with_filter)

# /xls ( Relatório completo do usuário - Todos os Budgets e expenses do cadastro )
# /xls?year=2022 ( Query param especificando ano do relatório )
# /xls?category_id=1 ( Query param especificando a categoria do expenses no relatório )
# /xls?year=2022&category_id=1 ( Query param reunindo as duas anteriores )
# /xls?initial_date=01/2022&final_date=04/2022 ( Query param para relatório de período )

# Relatório de badget específico
bp.get("/xls/<int:budget_id>")(reports_controller.report_with_filter_by_budget)



# ROTAS COM RETORNO EM .pdf

bp.get("/pdf")

# /pdf ( Relatório completo do usuário - Todos os Budgets e expenses do cadastro )
# /pdf?year=2022 ( Query param especificando ano do relatório )
# /pdf?category_id=1 ( Query param especificando a categoria do expenses no relatório )
# /pdf?year=2022&category_id=1 ( Query param reunindo as duas anteriores )
# /pdf?initial_date=01/2022&final_date=04/2022 ( Query param para relatório de período )

# Relatório de badget específico
bp.get("/pdf/<int:budget_id>")




# ROTAS DE ENVIO DE EMAIL

# ROTAS COM RETORNO EM .xls

bp.get("/xls_to_mail")

# /xls_to_mail ( Relatório completo do usuário - Todos os Budgets e expenses do cadastro )
# /xls_to_mail?year=2022 ( Query param especificando ano do relatório )
# /xls_to_mail?category_id=1 ( Query param especificando a categoria do expenses no relatório )
# /xls_to_mail?year=2022&category_id=1 ( Query param reunindo as duas anteriores )
# /xls_to_mail?initial_date=01/2022&final_date=04/2022 ( Query param para relatório de período )

# Relatório de badget específico
bp.get("/xls_to_mail/<int:budget_id>")



# ROTAS COM RETORNO EM .pdf

bp.get("/pdf_to_mail")

# /pdf_to_mail ( Relatório completo do usuário - Todos os Budgets e expenses do cadastro )
# /pdf_to_mail?year=2022 ( Query param especificando ano do relatório )
# /pdf_to_mail?category_id=1 ( Query param especificando a categoria do expenses no relatório )
# /pdf_to_mail?year=2022&category_id=1 ( Query param reunindo as duas anteriores )
# /pdf_to_mail?initial_date=01/2022&final_date=04/2022 ( Query param para relatório de período )

# Relatório de badget específico
bp.get("/pdf_to_mail/<int:budget_id>")


