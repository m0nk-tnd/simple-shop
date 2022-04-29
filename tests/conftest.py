import pytest

from sqlalchemy_utils import create_database, database_exists
from app.database import db
from .utils import generate_products


@pytest.fixture(scope='session')
def flask_app(pytestconfig):
    """Creates Flask app, which is then used for creating context and test client."""
    import app

    app.Config.SQLALCHEMY_DATABASE_URI = app.Config.SQLALCHEMY_DATABASE_URI.replace('ecom', 'ecom_test')

    yield app.create_app()


@pytest.fixture(scope='session', autouse=True)
def init_db(flask_app):
    """create db for tests."""
    if not database_exists(flask_app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(flask_app.config['SQLALCHEMY_DATABASE_URI'])
    with flask_app.app_context():
        db.drop_all()
        db.create_all()

        yield

        db.session.close()
        db.drop_all()


@pytest.fixture(scope='session')
def client(flask_app):
    """test client"""
    return flask_app.test_client()

