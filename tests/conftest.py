import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# Keep a copy of the original activity state for reset between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities() -> None:
    """Reset activities dict between tests to avoid state leakage."""
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def client() -> TestClient:
    """HTTP client for calling FastAPI endpoints."""
    return TestClient(app)
