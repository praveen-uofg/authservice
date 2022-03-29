import os
from unittest.mock import MagicMock

import pytest
from app.factories.application import setup_app


@pytest.fixture
def app():
    os.putenv("ENVIRONMENT", "testing")
    app = setup_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()