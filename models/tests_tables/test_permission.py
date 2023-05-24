from models.models import Permission
import pytest
from app import app, db


@pytest.fixture(scope='module')
def perm():
    perm = Permission(True, True, True)
    return perm


def test_add_user_to_database(perm):
    with app.app_context():
        db.session.add(perm)
        db.session.commit()
        assert perm in db.session
