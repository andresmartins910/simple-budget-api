from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Numeric, String, Integer
from dataclasses import dataclass


@dataclass
class BudgetModel(db.Model):
    id: int
    month: str
    year: str
    max_value: int
    user_id: int
    
    __tablename__ = "budget"

    id = Column(Integer, primary_key= True)
    month = Column(String(45), nullable = False)
    year = Column(String(45), nullable = False)
    max_value = Column(Numeric, nullable = False)
    user_id = Column(Integer, ForeignKey("user.id"))
