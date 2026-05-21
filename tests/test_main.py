"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""
import pytest
from litestar.testing import TestClient

from main import app
from app.model_utils import predict_churn


# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------

def test_predict_churn_basic():
    features = [
        650, "France", "Female", 35, 5,
        50000, 2, 1, 1, 75000
    ]

    result = predict_churn(features)

    assert result in [0, 1]


def test_predict_churn_edge_case():
    features = [
        0, "France", "Male", 0, 0,
        0, 0, 0, 0, 0
    ]

    result = predict_churn(features)

    assert result in [0, 1]


# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------

def test_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")

        assert response.status_code == 200
        assert "Churn Prediction API" in response.text


def test_predict_endpoint():
    payload = {
        "CreditScore": 650,
        "Geography": "France",
        "Gender": "Female",
        "Age": 35,
        "Tenure": 5,
        "Balance": 50000,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 75000
    }

    with TestClient(app=app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code == 201 or response.status_code == 200
        assert "prediction" in response.json()
        assert response.json()["prediction"] in [0, 1]


def test_health_endpoint_status():
    with TestClient(app=app) as client:
        response = client.get("/health")
        assert response.status_code == 200

def test_invalid_input():
    payload = {
        "CreditScore": "invalid", 
        "Geography": "France"
    }

    with TestClient(app=app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code == 400