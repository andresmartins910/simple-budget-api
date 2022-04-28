from app.configs.database import db
from sqlalchemy import Column, Integer, String, Date
from dataclasses import dataclass

from werkzeug.security import check_password_hash, generate_password_hash


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
    password_hash = Column(String(511), nullable = False, unique = True)


    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")

    
    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)


    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)