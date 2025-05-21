"""THIS MODULE LAUNCHES THE WEB SERVER"""

from flask import Flask, render_template, redirect, url_for, request
from sqlalchemy.exc import OperationalError
from pathlib import Path
from sproutware.db import db
from sproutware.models.seed import Seed
from sproutware.models.time import Time
from datetime import datetime as dt, timedelta

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
    return results
    
def generate_sunflower():
    seed = Seed(name = "sunflower", category = "flower")
    db.session.add(seed)
    db.session.commit()
    print(f'Seed Name: {seed.name}, Watered: {seed.is_watered}, Planted: {seed.is_planted}')
    return seed  

def generate_daisy():
    daisy = Seed(name = "Daisy", category = "flower", water_retention = timedelta(seconds=5), decay_interval = timedelta(seconds=5))
    db.session.add(daisy)
    db.session.commit()
    print(f'Seed Name: {daisy.name}, Watered: {daisy.is_watered}, Planted: {daisy.is_planted}')
    return daisy

def generate_cactus():
    cactus = Seed(name = "Cactus", category = "flower", water_retention = timedelta(seconds=30), decay_interval = timedelta(seconds=20))
    db.session.add(cactus)
    db.session.commit()
    print(f'Seed Name: {cactus.name}, Watered: {cactus.is_watered}, Planted: {cactus.is_planted}')
    return cactus  

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
    
    statement = db.select(Time).where(Time.id == 2)
    records = db.session.execute(statement)
    results = records.scalar()
    
    return render_template("home.html", results = results)

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

@app.route("/achievements")
def achievements():
    seeds = list(db.session.execute(db.select(Seed)).scalars())

    unlocked = {
        "game_started": len(seeds) > 0,
        "planted_sunflower": any(s.name.lower() == "sunflower" and s.is_planted for s in seeds),
        "planted_daisy": any(s.name.lower() == "daisy" and s.is_planted for s in seeds),
        "planted_cactus": any(s.name.lower() == "cactus" and s.is_planted for s in seeds),
        "first_water": any(s.is_watered for s in seeds),
        "first_death": any(s.is_dead if hasattr(s, "is_dead") else s.hp <= 0 for s in seeds),

        # New:
        "level_up": any(s.xp >= 100 for s in seeds),  # ⚡ Level Up!
        "fully_bloomed": all(
            any(s.name.lower() == name and s.produced_seeds for s in seeds)
            for name in ["sunflower", "daisy", "cactus"]
        ),  # 🏆 Fully Bloomed
    }

    # 🥇 Overachiever: all of the above must be True
    unlocked["overachiever"] = all(unlocked.values())

    return render_template("achievements.html", achievements=unlocked)


@app.route("/select/<int:seed_id>", methods=["POST"])
def select_seed(seed_id):
    selected_result = db.session.execute(db.select(Seed).where(Seed.is_selected == True)).scalar()
    if selected_result:
        selected_result.is_selected = False

    new_selected = db.get_or_404(Seed, seed_id)
    new_selected.is_selected = True
    db.session.commit()

    return redirect(url_for("inventory"))

@app.route("/plant_dead")
def dead_plant_static():
    return render_template("dead_plant.html")

@app.route("/plants_dead")
def dead_plants_static():
    return render_template("all_seeds_dead.html")

@app.route("/plant/<int:plant_id>")
def plant_page(plant_id):
    seed = db.session.execute(db.select(Seed).where(Seed.id == plant_id)).scalar()
    all_seeds = db.session.execute(db.select(Seed)).scalars().all()
    print(f"{seed} was loaded")
    print(f'List of all seeds: {all_seeds}')

    if len(all_seeds) == 0:
            seed = Seed(name = "Sunflower", category = "flower")
            db.session.add(seed)
            db.session.commit()
            print('A new sunflower has been generated!')
            return render_template("dead_plant.html")
    
    if seed == None:
        return render_template("dead_plant.html")

    if not seed:
        return f"Plant id not found.", 404

    time_update = call_time_update()

    player_start_time = (db.session.execute(db.select(Time).where(Time.id == 2))).scalar()
    countdown = seed.time_until_waterable()
    update_time()
    
    if seed.name == "sunflower" or seed.name == "Sunflower":
        if seed.produced_seeds == False:
            if seed.xp == 100:
                seed.produced_seeds = True
                seed.matured_time()
                generate_daisy()
                print('Your plant has fully matured! A new Daisy seed has been added to your inventory!')

    if seed.name == "Daisy" or seed.name == "daisy":
        if seed.produced_seeds == False:
            if seed.xp == 100:
                seed.produced_seeds = True
                seed.matured_time()
                generate_cactus()
                print('Your plant has fully matured! A new Cactus seed has been added to your inventory!')

    if seed.name == "cactus" or seed.name == "Cactus":
        if seed.produced_seeds == False:
            if seed.xp == 100:
                seed.produced_seeds = True
                seed.matured_time()
                generate_sunflower()
                generate_daisy()
                print('Your Cactus has fully matured! A new Sunflower and Daisy seed has been added to your inventory!')


    try:
        return render_template(
            "plant_page.html",  # ✅ this is your dynamic template
            plant=seed,
            start = player_start_time,
            time_update = time_update,
            countdown = countdown
        )
    
    except:
        return f"Template not found.", 404


# Allows user to plant an unplanted seed
@app.route("/plant/<int:seed_id>", methods=["POST"])
def plant_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    seed.plant()
    return redirect(url_for("plant_page", plant_id=seed.id))

# Allows user to water a seed if not watered
@app.route("/water/<int:seed_id>", methods=["POST"])
def water_seed(seed_id):
    seed = db.get_or_404(Seed, seed_id)
    msg = seed.water_plant()
    return redirect(url_for("plant_page", plant_id=seed.id, message=msg))

@app.route("/new", methods=["POST"])
def new_game():
    
    statement = db.select(Time).where(Time.id == 2)
    records = db.session.execute(statement)
    results = records.scalar()
    
    if results != None:
        return render_template("new_game_confirmation.html")
    
    began_game()
    generate_sunflower()
    
    return redirect(url_for("inventory"))
    # except Exception as e:
    #     print(f"Error creating new game: {e}")
    #     db.session.rollback()
    #     return redirect(url_for("home"))

@app.route("/new_game_confirmation", methods=["GET", "POST"])
def restart_game():
    if request.method == "POST":
        print('Resetting the database for a clear save....')
        delete_tables()
        create_tables()
        print('The database has been cleared.')
        return redirect(url_for("home"))
    
    # GET method — just show the confirmation page
    return render_template("new_game_confirmation.html")


# creates empty tables db
def create_tables():
    create = db.create_all()
    return create

# deletes all tables from db
def delete_tables():
    delete = db.drop_all()
    return delete

if __name__ == "__main__":
    app.run(debug=True, port=8888)
