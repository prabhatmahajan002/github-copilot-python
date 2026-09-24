import pytest

import app


@pytest.fixture
def client():
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None