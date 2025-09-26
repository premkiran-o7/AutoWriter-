from fastapi.testclient import TestClient
from app.main import app
from app.utils.logger import logger  # import logger

client = TestClient(app)

def test_generate_post_success():
    # Test successful post generation
    logger.info("Testing successful post generation")
    response = client.post("/generate-post", json={"topic": "Artificial Intelligence"})
    assert response.status_code == 200
    data = response.json()
    assert "topic" in data
    assert "linkedin_post" in data
    assert "news_sources" in data
    logger.info("Success response validated")

def test_generate_post_no_topic():
    # Test missing topic in request
    logger.info("Testing post generation with no topic")
    response = client.post("/generate-post", json={})
    assert response.status_code == 422  # Validation error
    logger.info("Validation error for missing topic confirmed")

