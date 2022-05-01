from datetime import date
from enum import unique
from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship, backref
from dataclasses import dataclass


@dataclass
class BudgetModel(db.Model):
    id: int
    month_year: str
    max_value: int
    user_id: int

    __tablename__ = "budget"

    id = Column(Integer, primary_key=True)
    month_year = Column(String, nullable=False, unique=True)
    max_value = Column(Numeric(10,2), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel", backref=backref("budgets", uselist=True), uselist=False)
