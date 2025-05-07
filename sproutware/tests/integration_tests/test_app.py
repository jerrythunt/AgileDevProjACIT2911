import pytest
from sproutware.app import app, db, call_time_update, began_game
from sproutware.models.seed import Seed
from sproutware.models.time import Time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"So you've been a gardner for" in response.data

def test_time_initialization(client):
    with app.app_context():
        result = call_time_update()
        assert isinstance(result, Time)
        assert result.name == "up_to_date"

def test_game_start_initialization(client):
    with app.app_context():
        result = began_game()
        assert isinstance(result, Time)
        assert result.name == "first_launch_date"

def test_plant_and_water_routes(client):
    with app.app_context():
        # 添加一个种子以供测试
        test_seed = Seed(name="Test Plant")
        db.session.add(test_seed)
        db.session.commit()

        # 测试 /plant 路由
        response_plant = client.post(f'/plant/{test_seed.id}')
        assert response_plant.status_code == 302  # Redirect

        # 测试 /water 路由
        response_water = client.post(f'/water/{test_seed.id}')
        assert response_water.status_code == 302



    def test_time_initialization(client):
        with app.app_context():
            result = call_time_update()
            assert isinstance(result, Time)
            assert result.name == "up_to_date"

    def test_game_start_initialization(client):
        with app.app_context():
            result = began_game()
            assert isinstance(result, Time)
            assert result.name == "first_launch_date"