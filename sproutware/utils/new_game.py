# sproutware/utils/db_utils.py

from sproutware import db
from sproutware.models.seed import Seed

def reset_game():
    db.drop_all()
    db.create_all()

    new_seed = Seed(name="Sunflower", hp=100)
    db.session.add(new_seed)
    db.session.commit()
