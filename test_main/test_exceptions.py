import sys 
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app


def test_get_tasks_with_nonexistent_build():
    with TestClient(app) as client:
        response = client.post('/get_tasks/', json={'build': 'nonexistent_build'})
        assert response.status_code == 404
        assert response.json() == {'detail': 'Build nonexistent_build not found'}


def test_get_tasks_with_empty_request():
    with TestClient(app) as client:
        response = client.post('/get_tasks/', json={})
        assert response.status_code == 400
        assert response.json() == {
            'detail': 'Request body must contain "build" field'}
