from app.configs.database import db
from sqlalchemy import Column, Integer, String, Date
from dataclasses import dataclass

@dataclass
class UserModel(db.Model):
    id: int
    name: str
    email: str
    phone: str
    cpf: str
    birthdate: str
    password_hash: str

    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    email = Column(String(70), nullable = False, unique = True)
    phone = Column(String(14), nullable = False, unique = True)
    cpf = Column(String(14), nullable = True)
    birthdate = Column(Date, nullable = True)
    password_hash = Column(String(100), nullable = False, unique = True)
