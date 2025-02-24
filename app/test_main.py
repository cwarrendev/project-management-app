from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Verify the response is HTML
    assert "text/html" in response.headers["content-type"]
    # Verify the welcome message is
    assert "Welcome" in response.text