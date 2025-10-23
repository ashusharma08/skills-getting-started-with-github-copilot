import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    # Use TestClient from FastAPI/Starlette
    with TestClient(app) as c:
        # Before each test, make a shallow copy of activities to restore
        original = {k: {**v, "participants": list(v["participants"])} for k, v in activities.items()}
        yield c
        # Restore activities to original state
        activities.clear()
        activities.update(original)
