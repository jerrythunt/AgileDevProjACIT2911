import pytest

from sproutware.app import app, db, call_time_update, began_game
from sproutware.models.seed import Seed
from sproutware.models.time import Time

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"So you've been a gardner for" in response.data

def test_plant_and_water_routes(client):
    with app.app_context():
        seed = Seed(name="Lavender")
        db.session.add(seed)
        db.session.commit()

        r1 = client.post(f'/plant/{seed.id}')
        r2 = client.post(f'/water/{seed.id}')
        assert r1.status_code == 302
        assert r2.status_code == 302
