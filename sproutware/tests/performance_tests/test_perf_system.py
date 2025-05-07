import pytest
from sproutware.app import app, db, call_time_update, began_game
from sproutware.models.seed import Seed
from sproutware.models.time import Time
import time

def test_time_update_performance(client):
    with app.app_context():
        start = time.time()
        call_time_update()
        duration = time.time() - start
        assert duration < 0.5  

def test_home_page_speed(client):
    start = time.time()
    response = client.get('/')
    duration = time.time() - start
    assert response.status_code == 200
    assert duration < 0.5  

