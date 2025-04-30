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

# A fixture to view all seeds in db
def call_seeds():
    statement = db.select(Seed)
    records = db.session.execute(statement)
    results = records.scalar()

    return results

# Calls current time from db 
def call_time_update():
    statement = db.select(Time).where(Time.id == 1)
    records = db.session.execute(statement)
    results = records.scalar()
 
    # If it doesn't exist yet (app has been initialized), store current time to database
    if results == None:
        current_time = Time(name = "up_to_date")
        db.session.add(current_time)
        db.session.commit()
        
        # Call recursively so it updates in one go
        call_time_update()
        return call_time_update()

    return results

def update_time():
    current_time_row = db.session.query(Time).first()
    current_time_row.current_time = dt.now()
    db.session.commit()

    return current_time_row

# Tell user when they first started playing
def began_game():  
    statement = db.select(Time).where(Time.id == 2)
    records = db.session.execute(statement)
    results = records.scalar()
 
    # If db entry doesnt exist (First time User), store the current time to database
    if results == None:
        began_time = Time(name = "first_launch_date")
        db.session.add(began_time)
        db.session.commit()
        
        # Call recursively so it updates in one go
        began_game()
        return began_game()

    return results

@app.route("/")
def home():
    seeds = call_seeds()
    # 'time_update' MUST run before 'start' (check pk's)
    time_update = call_time_update()
    start = began_game()
    update_time()

    return render_template("home.html", plant = seeds, time_update = time_update, start = start)

@app.route("/plant/<int:seed_id>", methods=["POST"])
def plant_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    seed.plant()
    
    return redirect(url_for("home"))

@app.route("/water/<int:seed_id>", methods=["POST"])
def water_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    seed.water_plant()
    
    return redirect(url_for("home"))


# @app.route("/flower1", methods=["GET", "POST"])
# def flower1():
#     message = None
#     image_filename = None  

#     if request.method == 'POST':
#         message = 'Seed planted!'
#         image_filename = "seed1.webp"

#     return render_template('flower.html', message=message, image=image_filename)

# For every planted seed in database
## check time_diff and apply business rules/logic that would've happened had it been running
## list their watered state - Completed
## list their growth stage  - Incomplete
## What else?

if __name__ == "__main__":
    app.run(debug = True, port = 8888)