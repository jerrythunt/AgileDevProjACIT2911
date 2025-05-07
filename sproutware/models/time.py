from db import db
from datetime import datetime as dt
from .seed import seed


# Classes are blueprints to create a real-world object
# Objects have attributes that define what they ARE (variable)
# Objects have methods that define what they DO (functions) 

# Create a table, inherit 'db.Model', otherwise it wont add to database!!
class Time(db.Model):
    # Declare the tablename
    __tablename__ = "Time"

    # Declare attributes that will populate database 
    # attribute = (db.mapped_column(db.DataType, options = insert_option))
    id = db.mapped_column(db.Integer, primary_key = True)
    name = db.mapped_column(db.String, nullable = False)
    current_time = db.mapped_column(db.DateTime, nullable = False, default = dt.now())