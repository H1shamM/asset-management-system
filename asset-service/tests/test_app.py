import pytest
from flask import json


@pytest.fixture(autouse=True)
def mock_dependencies(mocker):
    """Mocks database connections before app imports any dependencies"""
    # Mock MongoClient at its source
    mock_mongo = mocker.patch('pymongo.MongoClient')
    mock_mongo.return_value.admin.command.return_value = {'ok': 1}

    # Mock Redis client creation
    mock_redis = mocker.patch('redis.StrictRedis.from_url')
    mock_redis.return_value.ping.return_value = True

    # Now import app AFTER mocks are set up
    global app
    from app import app as imported_app
    app = imported_app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check_success(client):
    response = client.get('/health')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data == {"status": "OK"}


def test_health_check_mongo_failure(client, mocker):
    # Override MongoDB mock
    mocker.patch('databases.mongodb_setup.mongo_client.admin.command',
                 side_effect=Exception("MongoDB Down"))

    response = client.get('/health')
    data = json.loads(response.data)
    assert response.status_code == 500
    assert data['status'] == 'errors'
    assert data['message'] == "['MongoDB Error: MongoDB Down']"


def test_health_check_redis_failure(client, mocker):
    # Override Redis mock
    mocker.patch('databases.redis_setup.redis_client.ping',
                 side_effect=Exception("Redis Down"))
    response = client.get('/health')
    data = json.loads(response.data)
    assert response.status_code == 500
    assert data['status'] == 'errors'
    assert data['message'] == "['Redis Error: Redis Down']"


def test_health_check_both_fail(client, mocker):
    # Override both mocks
    mocker.patch('databases.mongodb_setup.mongo_client.admin.command',
                 side_effect=Exception("MongoDB Down"))
    mocker.patch('databases.redis_setup.redis_client.ping',
                 side_effect=Exception("Redis Down"))

    response = client.get('/health')
    data = json.loads(response.data)
    assert response.status_code == 500
    assert data['status'] == 'errors'
    # Python str() of the errors list
    assert data['message'] == "['MongoDB Error: MongoDB Down', 'Redis Error: Redis Down']"
