from fastapi.testclient import TestClient
from fastapi import Request
from app.main import app
from app.routes import get_sentiment_pipeline
from unittest.mock import MagicMock

client = TestClient(app)

def mock_get_sentiment_pipeline(request: Request):
    mock_pipeline = MagicMock()
    mock_pipeline.return_value = [[{'label': 'LABEL_2', 'score': 0.9817743301391602}, {'label': 'LABEL_1', 'score': 0.014286653138697147}, {'label': 'LABEL_0', 'score': 0.003938947804272175}]]
    return mock_pipeline

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyse_sentiment():
    app.dependency_overrides[get_sentiment_pipeline] = mock_get_sentiment_pipeline
    
    response = client.post('/analyse', json={"text": "The economy is improving."})
    assert response.status_code == 200
    assert len(response.json()["sentiments"]) > 0