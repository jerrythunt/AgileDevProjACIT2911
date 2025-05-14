"""THIS MODULE LAUNCHES THE WEB SERVER"""

from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy.exc import OperationalError
from pathlib import Path
from sproutware.db import db
from sproutware.models.seed import Seed
from sproutware.models.time import Time
from datetime import datetime as dt

"""INITIATES  APPLICATION, DO NOT TOUCH"""
app = Flask(__name__)

# name of database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Growing_Plants.db"
# populates database in current folder
app.instance_path = Path("./sproutware").resolve()

db.init_app(app)
"""DO NOT TOUCH ABOVE HERE ^"""

"""BEGINNING OF LOGIC STARTS HERE"""

# A fixture to view all seeds in db
def call_seeds():
    statement = db.select(Seed)
    records = db.session.execute(statement)
    results = records.scalar()

    # Added this to initialize a test seed in db for tests
    if not results:
        seed = Seed(name="TestPlant")
        db.session.add(seed)
        db.session.commit()
        results = seed

    results.decay_hp()
    return results

# Calls current time from db 
def call_time_update():
    statement = db.select(Time).where(Time.id == 1)
    records = db.session.execute(statement)
    results = records.scalar()

    if results is None:
        current_time = Time(name="up_to_date")
        db.session.add(current_time)
        db.session.commit()
        call_time_update()
        return call_time_update()

    return results

# Update the current time entry in database to right now
def update_time():
    statement = db.select(Time)
    records = db.session.execute(statement)
    current_time_row = records.scalars().first()
    current_time_row.current_time = dt.now()
    db.session.commit()
    return current_time_row

# Tell user when they first started playing the game
def began_game():
    statement = db.select(Time).where(Time.id == 2)
    records = db.session.execute(statement)
    results = records.scalar()

    if results is None:
        began_time = Time(name="first_launch_date")
        db.session.add(began_time)
        db.session.commit()
        began_game()
        return began_game()

    return results

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/continue")
def continue_game():
    return redirect(url_for("inventory"))

@app.route("/inventory")
def inventory():
    seeds = db.session.execute(db.select(Seed)).scalars().all()
    selected_seed = db.session.execute(db.select(Seed).where(Seed.is_selected == True)).scalar()

    selected_id = selected_seed.id if selected_seed else None
    return render_template("inventory.html", seeds=seeds, selected_id=selected_id)

@app.route("/select/<int:seed_id>", methods=["POST"])
def select_seed(seed_id):
    selected_result = db.session.execute(db.select(Seed).where(Seed.is_selected == True)).scalar()
    if selected_result:
        selected_result.is_selected = False

    new_selected = db.get_or_404(Seed, seed_id)
    new_selected.is_selected = True
    db.session.commit()

    return redirect(url_for("inventory"))

@app.route("/<plant_name>")
def plant_page(plant_name):
    seed = db.session.execute(db.select(Seed).where(Seed.name == plant_name)).scalar_one_or_none()
    if not seed:
        return f"Plant '{plant_name}' not found.", 404

    time_update = call_time_update()
    start = began_game()
    countdown = seed.time_until_waterable()
    update_time()

    return render_template("sunflower.html", plant=seed, time_update=time_update, start=start, countdown=countdown)

# Allows user to plant an unplanted seed
@app.route("/plant/<int:seed_id>", methods=["POST"])
def plant_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    seed.plant()
    return redirect(url_for("plant_page", plant_name=seed.name))

# Allows user to water a seed if not watered
@app.route("/water/<int:seed_id>", methods=["POST"])
def water_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    msg = seed.water_plant()
    return redirect(url_for("plant_page", plant_name=seed.name, message=msg))

@app.route("/new", methods=["POST"])
def new_game():
    try:
        seeds = db.session.execute(db.select(Seed)).scalars().all()
        for seed in seeds:
            db.session.delete(seed)
        times = db.session.execute(db.select(Time)).scalars().all()
        for time in times:
            db.session.delete(time)
        db.session.commit()

        seed = Seed(name="sunflower", category="flower")
        db.session.add(seed)

        current_time = Time(name="up_to_date")
        first_launch = Time(name="first_launch_date")
        db.session.add(current_time)
        db.session.add(first_launch)

        db.session.commit()
        return redirect(url_for("inventory"))
    except Exception as e:
        print(f"Error creating new game: {e}")
        db.session.rollback()
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
