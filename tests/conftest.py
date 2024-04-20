import pytest
import sys
from os.path import dirname as d
from os.path import abspath

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)


@pytest.fixture()
def app():
    from app.main import app as my_app

    return my_app


@pytest.fixture()
def db():
    from app.main import db as postgresql_db

    return postgresql_db


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
