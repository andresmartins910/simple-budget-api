from flask import Flask
from app.routes import (
    login_route,
    budgets_route,
    categories_route,
    expenses_route,
    reports_route,
    user_route,
)


def init_app(app: Flask):
    app.register_blueprint(login_route.bp)
    app.register_blueprint(user_route.bp)
    app.register_blueprint(budgets_route.bp)
    app.register_blueprint(categories_route.bp)
    app.register_blueprint(expenses_route.bp)
    app.register_blueprint(reports_route.bp)
