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
    
def test_create_user():
    response = client.post("/create-user")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "cwarren.dev@gmail.com"
    print("User created:", data)