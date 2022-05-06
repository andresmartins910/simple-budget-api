import os

from fpdf import FPDF
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime as dt


REPORTS_TEMP = os.getenv("REPORTS_TEMP")


def rel_pdf_time_year(payload, current_user):

    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author=payload['user'])
    pdf.set_title(title="relatorio anual")

    WIDTH = 210
    HEIGHT = 297
    TITLE = "RELATÓRIO - ANUAL"

    # titulo

    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(82)
    pdf.cell(20, 10, payload['year'],  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    all_budgets = payload['budgets']

    total_value = 0

    for budget in all_budgets:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(180, 9, dt.strftime((budget['month_year']), "%B/%Y"), border=1, ln=1, align='C')
        pdf.cell(40, 9, 'Nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'Data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'Valor', border=1, ln=0, align='C')
        pdf.cell(45, 9, 'Categoria', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:

            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, dt.strftime((expense['created_at']), "%d/%m/%Y"), border=1, ln=0, align='C')
            pdf.cell(40, 9, string_amount, border=1, ln=0, align='C')
            pdf.cell(45, 9, expense['category'], border=1, ln=1)
            if pdf.get_y() > 250.00:
                pdf.ln(10)
        pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de Gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    pdf.cell(10, 10, f"Lista de Budgets abordados", ln=1)
    pdf.set_font('Times', '', 11)
    for budget in all_budgets:
        pdf.cell(40, 9, dt.strftime((budget['month_year']), "%B/%Y"), border=1, ln=0, align='C')
        pdf.cell(1)
        if pdf.get_x() > 170:
            pdf.set_y(pdf.get_y()+10)
            pdf.set_x(10.001249999999999)
    pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do Usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output(f'app/{REPORTS_TEMP}/report.pdf', 'F')


def rel_pdf_time_month(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - MENSAL"


    # titulo
    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(60)
    pdf.cell(60, 7, f"Mês de referencia: {payload['budget']}")
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)


    # BUDGET
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 9, payload['budget'], border=1, ln=1, align="C")

    # COLUNAS
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(45, 9, 'Nome', border=1, ln=0, align='C')
    pdf.cell(55, 9, 'Data de criação', border=1, ln=0, align='C')
    pdf.cell(45, 9, 'Valor', border=1, ln=0, align='C')
    pdf.cell(45, 9, 'Categoria', border=1, ln=1, align='C')

    # EXPENSES
    pdf.set_font('Times', '', 11)
    total_value = 0
    for expense in payload['expenses']:
        total_value += expense['amount']
        string_amount = f" R$ {float(expense['amount'])}"
        pdf.cell(45, 9, expense['name'], border=1)
        pdf.cell(55, 9, dt.strftime(expense['created_at'], '%d/%m/%Y'), border=1, ln=0, align='C')
        pdf.cell(45, 9, string_amount, border=1, ln=0, align='C')
        pdf.cell(45, 9, expense['category'], border=1, ln=1)
        if pdf.get_y() > 250.00:
            pdf.ln(10)
    pdf.ln(7)

    # TOTAL DE GASTOS
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 8, f"Total de Gastos: ", border="B", ln=0)
    pdf.cell(30, 8, f"{total_value}", border='B', ln=0, align='C')
    pdf.ln(10)

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do Usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output(f'app/{REPORTS_TEMP}/report.pdf', 'F')


def rel_pdf_time_period(payload, current_user):
    pdf = FPDF('P', 'mm', 'A4')

    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_author(author= current_user['name'])
    TITLE = "RELATÓRIO - POR PERIDO"
    TIME = f"{dt.strftime(payload['initial_date'], '%d/%m/%Y')} - {dt.strftime(payload['final_date'], '%d/%m/%Y')}"

    pdf.cell(22)
    pdf.cell(150, 10, TITLE, border=1, ln=1, align='C')
    pdf.cell(82)
    pdf.cell(20, 10, TIME,  border=0, ln=1, align='C')
    pdf.line(10, 30, 200, 30)
    pdf.ln(20)

    pdf.set_font('Arial', 'B', 11)
    pdf.cell(40, 9, 'Nome', border=1, ln=0, align='C')
    pdf.cell(55, 9, 'Data de criação', border=1, ln=0, align='C')
    pdf.cell(40, 9, 'Valor', border=1, ln=0, align='C')
    pdf.cell(40, 9, 'Categoria', border=1, ln=1, align='C')

    total_value = 0
    pdf.set_font('Times', '', 11)
    for expense in payload['expenses']:
        total_value += expense['amount']
        string_amount = f" R$ {float(expense['amount'])}"
        pdf.cell(40, 9, expense['name'], border=1, ln=0)
        pdf.cell(55, 9, dt.strftime(expense['created_at'], '%d/%m/%Y'), border=1, ln=0, align='C')
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

    # DADOS DO USUARIO
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, f"Dados do usuário", ln=1)
    pdf.set_font('Times', '', 11)
    pdf.cell(70, 10, f"Nome: {current_user['name']}", border=1, ln=1)
    pdf.cell(70, 10, f"Email: {current_user['email']}", border=1, ln=1)
    pdf.cell(70, 10, f"Telefone: {current_user['phone']}", border=1, ln=1)

    pdf.output(f'app/{REPORTS_TEMP}/report.pdf', 'F')


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

    total_value = 0

    for budget in payload['budgets']:
        if pdf.get_x() > 250:
            pdf.ln(15)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(175, 9, dt.strftime((budget['month_year']), "%B/%Y"))[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'Nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'Data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'Valor', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'Categoria', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, dt.strftime(expense['created_at'], '%d/%m/%Y'), border=1, ln=0, align='C')
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
        pdf.cell(40, 9, dt.strftime((budget['month_year']), "%B/%Y"))[:10], border=1, ln=0, align='C')
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

    pdf.output(f'app/{REPORTS_TEMP}/report.pdf', 'F')


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
        pdf.cell(135, 9, dt.strftime((budget['month_year']), "%B/%Y"))[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'Nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'Data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'Valor', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, dt.strftime(expense['created_at'], '%d/%m/%Y'), border=1, ln=0, align='C')
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
        pdf.cell(40, 9, dt.strftime((budget['month_year']), "%B/%Y"))[:10], border=1, ln=0, align='C')
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

    pdf.output(f'app/{REPORTS_TEMP}/report.pdf', 'F')


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
        pdf.cell(135, 9, dt.strftime((budget['month_year']), "%B/%Y"))[:10], border=1, ln=1, align='C')
        pdf.cell(40, 9, 'Nome', border=1, ln=0, align='C')
        pdf.cell(55, 9, 'Data de criação', border=1, ln=0, align='C')
        pdf.cell(40, 9, 'Valor', border=1, ln=1, align='C')
        pdf.set_font('Times', '', 11)

        for expense in budget['expenses']:
            total_value += expense['amount']
            string_amount = f" R$ {float(expense['amount'])}"
            pdf.cell(40, 9, expense['name'], border=1, ln=0)
            pdf.cell(55, 9, dt.strftime(expense['created_at'], '%d/%m/%Y'), border=1, ln=0, align='C')
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
        pdf.cell(40, 9, dt.strftime((budget['month_year']), "%B/%Y"))[:10], border=1, ln=0, align='C')
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

    pdf.output(f'app/{REPORTS_TEMP}/report.pdf', 'F')


def normalize_amount(expenses):
    amount = []
    categories = []
    total = []

    for i in expenses:
        if(i.category.name in categories):
            for j in total:
                if(i.category.name == j["category"]):
                    j["amount"] = j["amount"] + i.amount

        else:
            amount.append(i.amount)
            categories.append(i.category.name)

            object = {
                "name": i.name,
                "description": i.description,
                "created_at": i.created_at,
                "category": i.category.name,
                "amount": i.amount
            }

            total.append(object)

    return total, categories


def create_pdf(categories, amount, title, xlabel):
    os.makedirs(f"app/{REPORTS_TEMP}", exist_ok=True)

    with PdfPages(f"app/{REPORTS_TEMP}/chart_report.pdf") as pdf:

        plt.rcParams["figure.figsize"] = (7, 6)
        plt.bar(categories, amount)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel("Despesas", fontsize=12)

        plt.xticks(categories, rotation=20)

        plt.title(title)

        pdf.savefig()
        plt.close()

