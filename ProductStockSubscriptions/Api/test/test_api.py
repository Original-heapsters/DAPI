import pytest
from ..app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Expect hello world response"""

    rv = client.get('/')
    assert b'Hello World!' in rv.data
