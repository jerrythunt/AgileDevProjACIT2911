from db import db
from datetime import datetime as dt
from app import app
from models import Time, Seed
import time
from sqlalchemy.exc import OperationalError

def create_tables():
    # creates empty tables
    create = db.create_all()
    return create

def delete_tables():
    # deletes all tables
    delete = db.drop_all()
    return delete

# def start_time():
#     sessions_start_time = dt.now()
#     print(f'Sessions Start Time: {sessions_start_time}. The class type is {type(sessions_start_time)}')
#     return sessions_start_time

def generate_seed():
    seed = Seed(name = "daisy", category = "flower")
    db.session.add(seed)
    db.session.commit()
    print(f'Seed Name: {seed.name}, Watered: {seed.is_watered}, Planted: {seed.is_planted}')
    return seed    

if __name__ == "__main__":
    with app.app_context():
        delete_tables()
        create_tables()
        generate_seed()
        # init_time = start_time()
        # # result = db.session.execute(db.select(dt.now())).scalar()
        # # print(f'The application started at:", {str(result)}. The type is {type(result)}')
        # time_keeper()
