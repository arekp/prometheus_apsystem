import pytest
import requests_mock
import requests
import prometheus_apsystem
import codecs
from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()   

@pytest.fixture()
def realtimedata():
    f=codecs.open("tests/realtimedata.html", 'r', 'utf-8')
    return f.read()

@pytest.fixture()
def indexdata():
    f=codecs.open("tests/index.html", 'r', 'utf-8')
    return f.read()

def test_converttab(requests_mock,realtimedata):
    requests_mock.get('http://test.com', text=realtimedata)
    print(prometheus_apsystem.converttab(requests.get('http://test.com')))
    assert len(prometheus_apsystem.converttab(requests.get('http://test.com'))) > 0

def test_index(app, client):
    res = client.get('/metrics')
    assert res.status_code == 200
    assert b'panele_lifetimegeneration' in res.data
    