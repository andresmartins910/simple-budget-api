from dataclasses import dataclass

from app.configs.database import db
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates


@dataclass
class CategoryModel(db.Model):

    id : int
    name : str
    description : str


    __tablename__ = "category"


    id = Column(Integer, primary_key = True)
    name = Column(String(45), nullable = False)
    description = Column(String(90), nullable = False)
    created_by = Column(String(20), nullable = False)

    @validates('name', 'description')
    def validate_keys(self, key, value):

        if type(value) != str:
            raise TypeError(description=f"Invalid type for key '{key}'; it should be `string`.")

        if key == 'name':
            return value.title()
        if key == 'description':
            return value
