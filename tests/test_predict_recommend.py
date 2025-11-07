"""
Unit tests for the predict and recommend endpoints using FastAPI TestClient.
These tests exercise the endpoints without requiring an external running server.
They will skip when the application returns 503 (model or vector store not ready).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predict_endpoint_valid_input():
    """POST /predict with valid text should return a label and confidence or 503 if model not ready."""
    response = client.post("/predict", json={"text": "This movie was absolutely fantastic!"})

    if response.status_code == 503:
        pytest.skip("Model not loaded")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "label" in data and "confidence" in data
    assert data["label"] in ["positive", "negative"]
    # confidence may be int/float depending on serialization
    conf = float(data["confidence"]) if data["confidence"] is not None else None
    assert conf is not None and 0.0 <= conf <= 1.0


def test_predict_endpoint_invalid_input():
    """Empty text and missing text field should return 422 Unprocessable Entity."""
    # Empty text
    response = client.post("/predict", json={"text": ""})
    if response.status_code == 503:
        pytest.skip("Model not loaded")
    assert response.status_code == 422

    # Missing text field
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_recommend_endpoint_success():
    """POST /recommend should return recommended_products list or 503 if vector store unavailable."""
    response = client.post("/recommend", json={"text": "Looking for a fast laptop"})

    if response.status_code == 503:
        pytest.skip("Vector store not available for recommendations")

    assert response.status_code == 200
    data = response.json()
    assert "recommended_products" in data
    assert isinstance(data["recommended_products"], list)


def test_recommend_detailed_endpoint_success():
    """POST /recommend/detailed should return detailed recommendations or 503 if vector store unavailable."""
    response = client.post("/recommend/detailed", json={"text": "wireless headphones"})

    if response.status_code == 503:
        pytest.skip("Vector store not available for recommendations")

    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)

    if data["recommendations"]:
        rec = data["recommendations"][0]
        assert "product_id" in rec
        assert "product_title" in rec
        assert "similarity_score" in rec


def test_recommend_endpoint_invalid_input():
    """Empty text and missing text field for /recommend should produce 422."""
    response = client.post("/recommend", json={"text": ""})
    assert response.status_code == 422

    response = client.post("/recommend", json={})
    assert response.status_code == 422
 