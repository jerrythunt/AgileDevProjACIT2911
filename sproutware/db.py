"""THIS MODULE ALLOWS INHERITANCE SO CLASSES WILL HAVE DATABASE CREATION/TABLE GENERATION """
"""DO NOT TOUCH ANYTHING ON THIS PAGE"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# This is the blueprint for all classes in in models.py that give them database functionality
class Base(DeclarativeBase):
    pass

# Allows database functionality to be called with 'db.'
db = SQLAlchemy(model_class=Base)