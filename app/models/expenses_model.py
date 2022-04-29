from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime
from dataclasses import dataclass


@dataclass
class ExpenseModel(db.Model):
    id: int
    name: str
    description: str
    created_at: str
    amount: float

    __tablename__ = "expense"

    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    description = Column(String(45), nullable=True)
    created_at = Column(DateTime, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    budget_id = Column(Integer, ForeignKey("budget.id"))
    category_id = Column(Integer, ForeignKey("category.id"))

    budget = db.relationship("BudgetModel", backref="expenses")
    category = db.relationship("CategoryModel", backref="expenses")
