from app.configs.database import db
from sqlalchemy import Column, ForeignKey, Numeric, Integer, String
from sqlalchemy.orm import relationship, backref, validates
from dataclasses import dataclass
from app.exceptions import InvalidDataTypeError


@dataclass
class BudgetModel(db.Model):

    id: int
    month_year: str
    max_value: int
    # user_id: int

    __tablename__ = "budget"

    id = Column(Integer, primary_key=True)
    month_year = Column(String, nullable=False)
    max_value = Column(Numeric(10,2), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel", backref=backref("budgets", uselist=True), uselist=False)

    @validates('month_year')
    def validate_keys(self, key, value):

        if type(value) != str:
            raise InvalidDataTypeError(description=f"Invalid type for key '{key}'; it should be `string`.")

        return value

    @validates('max_value')
    def validate_keys(self, key, value):

        if type(value) != float and type(value) != int:

            raise InvalidDataTypeError(description=f"Invalid type for key '{key}'; it should be `monetary`.")

        return value
