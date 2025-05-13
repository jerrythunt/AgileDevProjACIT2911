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
app.instance_path = Path(".").resolve()

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
        results=seed

    results.decay_hp()

    return results

# Calls current time from db 
def call_time_update():
    # Query the database for a Time table, and grab the specific entry where the id == 1
    statement = db.select(Time).where(Time.id == 1)
    # Execute the statement
    records = db.session.execute(statement)
    # Convert the statement/query to an object so we can use it (.scalar()/.scalars()) 
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

# Update the current time entry in database to right now
def update_time():
    # Query the database for a table named Time, and grab the first row
    current_time_row = db.session.query(Time).first()
    # Update the first row to current time 
    current_time_row.current_time = dt.now()
    # Commit the change to the database
    db.session.commit()

    return current_time_row

# Tell user when they first started playing the game
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
    return render_template("home.html")

@app.route("/continue")
def continue_game():
    return redirect(url_for("inventory"))



@app.route("/inventory")
def inventory():
    seeds = db.session.execute(db.select(Seed)).scalars().all()

    selected_seed = db.session.execute(db.select(Seed).where(Seed.is_selected == True)).scalar()

    if selected_seed:
        selected_id = selected_seed.id
    else:
        selected_id = None

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



@app.route("/sunflower")
def sunflower():
    seeds = call_seeds()
    # 'time_update' MUST run before 'start' (check pk's)
    time_update = call_time_update()
    start = began_game()
    # countdown = 5.00 - (seeds.time_until_waterable()).total_seconds()
    
    countdown = seeds.time_until_waterable()
    # if check == None:
    #     countdown = "There is no countdown"
    # elif check != None:
    #     countdown = check
    # else:
    #     pass
        
    update_time()
    

    # use the "home.html" template, store the result of each function to a variable that can be called in the html file. Ex: {{plant.name}}
    return render_template("sunflower.html", plant = seeds, time_update = time_update, start = start, countdown = countdown)

# # Home page of app
# @app.route("/")
# # When home page is loaded, run these functions
# def home():
#     seeds = call_seeds()
#     # 'time_update' MUST run before 'start' (check pk's)
#     time_update = call_time_update()
#     start = began_game()
#     update_time()

#     # use the "home.html" template, store the result of each function to a variable that can be called in the html file. Ex: {{plant.name}}
#     return render_template("home.html", plant = seeds, time_update = time_update, start = start)

# Allows user to plant an unplanted seed
@app.route("/plant/<int:seed_id>", methods=["POST"])
def plant_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    seed.plant()
    
    return redirect(url_for("sunflower"))

# Allows user to water a seed if not watered
@app.route("/water/<int:seed_id>", methods=["POST"])
def water_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    msg = seed.water_plant()

    return redirect(url_for("sunflower", message=msg))




# When app.py is run, it runs in debug mode on localhost:8888 
if __name__ == "__main__":
    app.run(debug = True, port = 8888)