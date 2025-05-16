"""THIS MODULE ALLOWS DATABASE TABLE GENERATION"""

from sproutware.db import db
from datetime import datetime as dt
from sproutware.app import app
from sproutware.models.seed import Seed
from sproutware.models.time import Time

# creates empty tables db
def create_tables():
    create = db.create_all()
    return create

# deletes all tables from db
def delete_tables():
    delete = db.drop_all()
    return delete

# Create a 'seed' object
def generate_seed():
    # Call Seed class, and input necessary attributes
    seed = Seed(name = "Sunflower", category = "flower")
    # seed2 = Seed(name = "Daisy", category = "flower")
    # seed3 = Seed(name = "Cactus", category = "flower")
    # Add the new object to the current session
    # db.session.add_all([seed, seed2, seed3])
    db.session.add(seed)
    db.session.commit()
    # Commit the new object to the database
    # Print the objects attributes for debugging purposes
    print(f'Seed Name: {seed.name}, Watered: {seed.is_watered}, Planted: {seed.is_planted}')
    # Return the newly created object
    return seed    

# if you run "manage.py"/ "python -m sproutware.manage"
if __name__ == "__main__":
    # given the context of app 
    with app.app_context():
        delete_tables()
        create_tables()
        generate_seed()
