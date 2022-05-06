from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import validates, backref, relationship
from dataclasses import dataclass
import re
from app.exceptions.users_exceptions import PhoneExc, CPFExc, BirthdateExc
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class UserModel(db.Model):
    id: int
    name: str
    email: str
    phone: str
    cpf: str
    birthdate: str

    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    email = Column(String(70), nullable = False, unique = True)
    phone = Column(String(14), nullable = False, unique = True)
    cpf = Column(String(14), nullable = True, unique = True)
    birthdate = Column(DateTime, nullable = True)
    password_hash = Column(String(511), nullable = False, unique = True)


    @validates("phone")
    def validate_phone(self, key, value):
        reg = re.findall("^\(\d{2}\)\d{5}-\d{4}$", value)

        if(reg):
            return reg[0]
        else:
            raise PhoneExc("Phone Format must be: (41)99999-9999")


    @validates("cpf")
    def validate_cpf(self, key, value):
        reg = re.findall("\d{3}.\d{3}.\d{3}-\d{2}$", value)

        if(reg):
            return reg[0]
        else:
            raise CPFExc("CPF Format must be: 111.222.333-44")

    @validates("birthdate")
    def validate_birthdate(self, key, value):
        try:
            date = datetime.strptime(value, "%d/%m/%Y")
        except:
            raise BirthdateExc("Birthdate format must be: dd/mm/YYYY")

        return date

    @property
    def password(self):
        raise AttributeError("Password cannot be accessed")


    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)


    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)