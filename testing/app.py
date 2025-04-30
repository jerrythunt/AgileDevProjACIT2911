from flask import Flask, render_template, redirect, url_for, jsonify, request
from sqlalchemy.exc import OperationalError
from pathlib import Path
from db import db
from models import Time, Seed
from datetime import datetime as dt
import time

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Growing_Plants.db"
app.instance_path = Path(".").resolve()

db.init_app(app)

start_of_session = dt.now()

def call_seedss():
    statement = db.select(Seed)
    records = db.session.execute(statement)
    results = records.scalar()
    return results


@app.route("/")
def home():
    seeds = call_seedss()

    return render_template("home.html", data = start_of_session, plant = seeds)


# For every planted seed in database
## check time_diff and apply business rules/logic that would've happened had it been running
## list their watered state
## list their growth stage 
## list if 

if __name__ == "__main__":
    app.run(debug = True, port = 8888)


# def time_keeper():

#     current_time_row = db.session.query(Time).first()
#     if not current_time_row:
#         current_time_row = Time(current_time= dt.now())
#         db.session.add(current_time_row)
#         db.session.commit()

#     try:
#         while True:
#             try:
#                 current_time_row.current_time = dt.now()
#                 db.session.commit()
#                 # print(f'The current time is: {current_time_row.current_time}')
#             except OperationalError as e:
#                 print("Database is locked. Rolling commit back and retrying in 5.0 seconds...")
#                 db.session.rollback()  # important: undo the failed transaction
#                 time.sleep(5)  # wait and retry
#                 continue
#             time.sleep(1)  # normal delay
#     except KeyboardInterrupt:
#         print("Stopped updating.")
#     finally:
#         db.session.close()