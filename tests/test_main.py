from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyse_sentiment():
    response = client.post('/analyse', json={"text": "The economy is improving."})
    assert response.status_code == 200
    assert len(response.json()["sentiments"]) > 0