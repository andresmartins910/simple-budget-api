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


def rel_pdf_time_year(year, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    pdf.set_title(title = "relatorio anual")

    WIDTH = 210
    HEIGHT = 297
    TITLE = "RELATÓRIO - POR ANO"

    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(82)
    pdf.cell(20, 10, year,  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    session: Session = db.session
    all_budgets: BaseQuery = session.query(BudgetModel)
    all_budgets: Query = (
        session.query(BudgetModel)
        .join(UserModel)
        .filter(BudgetModel.user_id == current_user["id"])
        .all()
    )
    years_budgets = [budget for budget in all_budgets if budget.month_year[3:] == year]

    # pdf.page_no() # retorna o numero da pagina
    total_value = 0

    for budget in years_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(120, 9, budget.month_year, border=1, ln=1)
        pdf.cell(60,9, 'expense name', border=1, ln=0)
        pdf.cell(60,9, 'expense amount', border=1, ln=1)
        pdf.set_font('Times', '', 11)

        for expense in budget.expenses:
            total_value += expense.amount
            string_amount = f" R$ {float(expense.amount)}"
            pdf.cell(60, 9, expense.name, border=1)
            pdf.cell(60, 9, string_amount, ln=1, border=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)
    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)

    pdf.set_font('Times', '', 11)
    for budget in years_budgets:
        pdf.cell(40, 9, budget.month_year, border=1, ln=0)
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_year.pdf', 'F')

    # webbrowser.open_new('app/services/relatoriotest_year.pdf') #abre o PDF no navegador padrão, apenas para teste

def rel_pdf_time_month(month, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - POR MÊS"


    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(67)
    pdf.cell(60, 7, f'mês de referencia: {month}')
    pdf.ln(20)

    session: Session = db.session

    user = session.query(UserModel).filter(UserModel.id == current_user['id']).first()
    all_budgets = user.budgets
    budget_month = []
    for budget in all_budgets:
        if budget.month_year[:2] == month:
            budget_month.append(budget)

    total_value = 0

    for budget in budget_month:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(120, 9, budget.month_year, border=1, ln=1)
        pdf.cell(60,9, 'expense name', border=1, ln=0)
        pdf.cell(60,9, 'expense amount', border=1, ln=1)
        pdf.set_font('Times', '', 11)

        for expense in budget.expenses:
            total_value += expense.amount
            string_amount = f" R$ {float(expense.amount)}"
            pdf.cell(60, 9, expense.name, border=1)
            pdf.cell(60, 9, string_amount, ln=1, border=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)


    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)
    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)

    pdf.set_font('Times', '', 11)
    for budget in budget_month:
        pdf.cell(40, 9, budget.month_year, border=1, ln=0)
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_month.pdf', 'F')

    # webbrowser.open_new('app/services/relatoriotest_month.pdf') #abre o PDF no navegador padrão, apenas para teste

def rel_pdf_time_period(start_time, end_time, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - POR PERIDO"
    TIME = f"{start_time} - {end_time}"

    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(82)
    pdf.cell(20, 10, TIME,  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    session: Session = db.session

    all_budgets: BaseQuery = session.query(BudgetModel)
    all_budgets: Query = (
        all_budgets
        .select_from(BudgetModel)
        .join(UserModel)
        .filter(UserModel.id == current_user['id'])
        .filter(BudgetModel.month_year.between(start_time, end_time))
        .all()
    )

    # pdf.page_no() # retorna o numero da pagina
    total_value = 0

    for budget in all_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(120, 9, budget.month_year, border=1, ln=1)
        pdf.cell(60,9, 'expense name', border=1, ln=0)
        pdf.cell(60,9, 'expense amount', border=1, ln=1)
        pdf.set_font('Times', '', 11)

        for expense in budget.expenses:
            total_value += expense.amount
            string_amout = f" R$ {float(expense.amount)}"
            pdf.cell(60, 9, expense.name, border=1)
            pdf.cell(60, 9, string_amout, ln=1, border=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)
    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)

    pdf.set_font('Times', '', 11)
    for budget in all_budgets:
        pdf.cell(40, 9, budget.month_year, border=1, ln=0)
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_period.pdf', 'F')


def rel_all_budget(current_user):
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - COMPLETO"

    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    session: Session = db.session

    user = session.query(UserModel).filter(UserModel.id == current_user['id']).first()
    all_budgets = user.budgets

    # pdf.page_no() # retorna o numero da pagina
    total_value = 0

    for budget in all_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(120, 9, budget.month_year, border=1, ln=1)
        pdf.cell(60,9, 'expense name', border=1, ln=0)
        pdf.cell(60,9, 'expense amount', border=1, ln=1)
        pdf.set_font('Times', '', 11)

        for expense in budget.expenses:
            total_value += expense.amount
            string_amout = f" R$ {float(expense.amount)}"
            pdf.cell(60, 9, expense.name, border=1)
            pdf.cell(60, 9, string_amout, ln=1, border=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)
    pdf.cell(10, 10, f"Lista de budgets abordados", ln=1)

    pdf.set_font('Times', '', 11)
    for budget in all_budgets:
        pdf.cell(40, 9, budget.month_year, border=1, ln=0)
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output('app/reports_temp/relatoriotest_complet.pdf', 'F')


def download_file(file_name):
    try:
        return send_from_directory(
            directory=f"app/services",
            path=f"{file_name}",
            as_attachment=True
        )
    except:
        print('error')
