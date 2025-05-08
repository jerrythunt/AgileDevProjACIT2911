import pytest
from sproutware.app import app, db

@pytest.fixture(scope="session")
def setup_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

@pytest.fixture
def client(setup_db):  
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
