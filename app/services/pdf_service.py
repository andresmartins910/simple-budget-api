import os
import webbrowser

from flask import send_from_directory
from app.configs.database import db
from app.models.budgets_model import BudgetModel
from app.models.categories_model import CategoryModel
from app.models.expenses_model import ExpenseModel
from app.models.users_model import UserModel
from flask_sqlalchemy import BaseQuery
from fpdf import FPDF
from sqlalchemy.orm import Query, Session
from werkzeug.utils import secure_filename


def rel_pdf_time_year(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author=payload['user'])
    pdf.set_title(title="relatorio anual")

    WIDTH = 210
    HEIGHT = 297
    TITLE = "RELATÓRIO - POR ANO"

    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(82)
    pdf.cell(20, 10, payload['year'],  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    # session: Session = db.session
    # all_budgets: BaseQuery = session.query(BudgetModel)
    # all_budgets: Query = (
    #     session.query(BudgetModel)
    #     .join(UserModel)
    #     .filter(BudgetModel.user_id == payload['user'])
    #     .all()
    # )
    all_budgets = payload['budgets']
    # years_budgets = [budget for budget in all_budgets if budget['month_year'][3:] == payload['year']]

    # pdf.page_no() # retorna o numero da pagina
    total_value = 0
    for budget in all_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(135, 9, str(budget['month_year'])[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'valor', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            # print('-'*100)
            # print(expense)
            # print('-'*100)
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, str(expense['created_at']), border=1, ln=0, align='C')
            pdf.cell(40, 9, string_amount, border=1, ln=1, align='C')
            # pdf.cell(45, 9, expense['category'], border=1, ln=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)
    pdf.set_font('Times', '', 11)
    for budget in all_budgets:
        pdf.cell(40, 9, str(budget['month_year'])[:10], border=1, ln=0, align='C')
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_year.pdf', 'F')

    # webbrowser.open_new('app/services/relatoriotest_year.pdf') #abre o PDF no navegador padrão, apenas para teste

def rel_pdf_time_month(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - POR MÊS"


    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(60)
    pdf.cell(60, 7, f"mês de referencia: {payload['budget']}")
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    # session: Session = db.session

    # user = session.query(UserModel).filter(UserModel.id == current_user['id']).first()
    # all_budgets = user.budgets
    # budget_month = []
    # for budget in all_budgets:
    #     if budget['month_year'][:2] == month:
    #         budget_month.append(budget)


    # for budget in budget_month:
    #     if pdf.get_x() > 250:
    #         pdf.ln(15)
    #     pdf.set_font('Arial', 'B', 11)
    #     pdf.cell(120, 9, str(budget['month_year'])[:10], border=1, ln=1, align='C')
    #     pdf.cell(60,9, 'expense name', border=1, ln=0)
    #     pdf.cell(60,9, 'expense amount', border=1, ln=1)
    #     pdf.set_font('Times', '', 11)

    # BUDGET
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 9, payload['budget'], border=1, ln=1, align="C")

    # COLUNAS
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(45, 9, 'nome', border=1, ln=0, align='C')
    pdf.cell(55, 9, 'data de criação', border=1, ln=0, align='C')
    pdf.cell(45, 9, 'valor', border=1, ln=0, align='C')
    pdf.cell(45, 9, 'categoria', border=1, ln=1, align='C')

    # EXPENSES
    pdf.set_font('Times', '', 11)
    total_value = 0
    for expense in payload['expenses']:
        total_value += expense['amount']
        string_amount = f" R$ {float(expense['amount'])}"
        pdf.cell(45, 9, expense['name'], border=1)
        pdf.cell(55, 9, str(expense['created_at']), border=1, ln=0, align='C')
        pdf.cell(45, 9, string_amount, border=1, ln=0, align='C')
        pdf.cell(45, 9, expense['category'], border=1, ln=1)
        if pdf.get_y() > 250.00:
            pdf.ln(10)
    pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    # pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)
    # pdf.set_font('Times', '', 11)
    # for budget in budget_month:
    #     pdf.cell(40, 9, str(budget['month_year'])[:10], border=1, ln=0, align='C')
    #     pdf.cell(1)
    #     if pdf.get_x() > 170:
    #         pdf.set_y(pdf.get_y()+10)
    #         pdf.set_x(10.001249999999999)
    # pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_month.pdf', 'F')

    # webbrowser.open_new('app/services/relatoriotest_month.pdf') #abre o PDF no navegador padrão, apenas para teste

def rel_pdf_time_period(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - POR PERIDO"
    TIME = f"{payload['initial_date']} - {payload['final_date']}"

    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(82)
    pdf.cell(20, 10, TIME,  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    # session: Session = db.session

    # all_budgets: BaseQuery = session.query(BudgetModel)
    # all_budgets: Query = (
    #     all_budgets
    #     .select_from(BudgetModel)
    #     .join(UserModel)
    #     .filter(UserModel.id == current_user['id'])
    #     .filter(BudgetModel.month_year.between(start_time, end_time))
    #     .all()
    # )

    # pdf.page_no() # retorna o numero da pagina

    # for budget in all_budgets:
    #     if pdf.get_x() > 250:
    #         pdf.ln(15)
    #     pdf.set_font('Arial', 'B', 11)
    #     pdf.cell(120, 9, str(budget['month_year'])[:10], border=1, ln=1, align='C')
    #     pdf.cell(60,9, 'expense name', border=1, ln=0)
    #     pdf.cell(60,9, 'expense amount', border=1, ln=1)
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 9, 'nome', border=1, ln=0, align='C')
    pdf.cell(55, 9, 'data de criação', border=1, ln=0, align='C')
    pdf.cell(40, 9, 'valor', border=1, ln=0, align='C')
    pdf.cell(40, 9, 'categoria', border=1, ln=1, align='C')
    
    total_value = 0
    pdf.set_font('Times', '', 11)
    for expense in payload['expenses']:
        total_value += expense['amount']
        string_amount = f" R$ {float(expense['amount'])}"
        pdf.cell(40, 9, expense['name'], border=1, ln=0)
        pdf.cell(55, 9, str(expense['created_at']), border=1, ln=0, align='C')
        pdf.cell(40, 9, string_amount, border=1, ln=0, align='C')
        pdf.cell(40, 9, expense['category'], border=1, ln=1)
        if pdf.get_y() > 250.00:
            pdf.ln(10)
    pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    # pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)
    # pdf.set_font('Times', '', 11)
    # for budget in all_budgets:
    #     pdf.cell(40, 9, str(budget['month_year'])[:10], border=1, ln=0, align='C')
    #     pdf.cell(1)
    #     if pdf.get_x() > 170:
    #         pdf.set_y(pdf.get_y()+10)
    #         pdf.set_x(10.001249999999999)
    # pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_period.pdf', 'F')


def rel_all_budget(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - COMPLETO"

    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    # session: Session = db.session
    # user = session.query(UserModel).filter(UserModel.id == current_user['id']).first()
    # all_budgets = user.budgets

    # pdf.page_no() # retorna o numero da pagina
    total_value = 0

    for budget in payload['budgets']:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(175, 9, str(budget['month_year'])[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'valor', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'categoria', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, str(expense['created_at']), border=1, ln=0, align='C')
            pdf.cell(40, 9, string_amount, border=1, ln=0, align='C')
            pdf.cell(40, 9, expense['category'], border=1, ln=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)
    pdf.set_font('Times', '', 11)
    for budget in payload['budgets']:
        pdf.cell(40, 9, str(budget['month_year'])[:10], border=1, ln=0, align='C')
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_complet.pdf', 'F')


def rel_by_category(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author=payload['user'])
    pdf.set_title(title="relatorio categoria")
    TITLE = "RELATÓRIO - POR CATEGORIA"

    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(83)
    pdf.cell(20, 10, f"Categoria: {payload['category']}",  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    all_budgets = payload['budgets']

    total_value = 0
    for budget in all_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(135, 9, str(budget['month_year'])[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'valor', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, str(expense['created_at']), border=1, ln=0, align='C')
            pdf.cell(40, 9, string_amount, border=1, ln=1, align='C')
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)
    pdf.set_font('Times', '', 11)
    for budget in all_budgets:
        pdf.cell(40, 9, str(budget['month_year'])[:10], border=1, ln=0, align='C')
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_categorie.pdf', 'F')


def rel_by_category_year(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author=payload['user'])
    pdf.set_title(title="relatorio categoria")
    TITLE = "RELATÓRIO - POR CATEGORIA E ANO"

    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(83)
    pdf.cell(20, 10, f"{payload['category']} - {payload['year']}",  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    all_budgets = payload['budgets']

    total_value = 0
    for budget in all_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(135, 9, str(budget['month_year'])[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'valor', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, str(expense['created_at']), border=1, ln=0, align='C')
            pdf.cell(40, 9, string_amount, border=1, ln=1, align='C')
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)
    pdf.set_font('Times', '', 11)
    for budget in all_budgets:
        pdf.cell(40, 9, str(budget['month_year'])[:10], border=1, ln=0, align='C')
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_categorie_year.pdf', 'F')
    ...


def download_file(file_name):
    try:
        return send_from_directory(
            directory=f"app/services",
            path=f"{file_name}",
            as_attachment=True
        )
    except:
        print('error')
