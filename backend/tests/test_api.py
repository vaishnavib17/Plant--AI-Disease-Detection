"""
PlantCare AI - Automated Backend Tests
Validates FastAPI endpoints, health checks, class mappings, and prediction responses.
"""

import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True

def test_get_classes():
    response = client.get("/classes")
    assert response.status_code == 200
    data = response.json()
    assert "classes" in data
    assert data["total_classes"] == 16

def test_get_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "EfficientNetB0" in data["models"]
    assert "CustomCNN" in data["models"]
