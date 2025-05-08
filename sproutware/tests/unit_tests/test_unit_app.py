import pytest
from sproutware.app import app, db, call_time_update, began_game
from sproutware.models.seed import Seed
from sproutware.models.time import Time

def test_seed_initial_hp():
    seed = Seed(name="sunflower", hp=100)
    assert seed.hp == 100

def test_time_default_name():
    time = Time(name="test")
    assert time.name == "test"
