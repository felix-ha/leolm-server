from fastapi.testclient import TestClient
from server import app  
import pytest
from config import configuration
from model_api import ServerStatus, LLMResponse


@pytest.fixture
def client():
    return TestClient(app)


def test_status(client):
    response = client.get(configuration.server.routes.status)
    server_status = ServerStatus.model_validate(response.json())
    assert response.status_code == 200
    assert server_status == ServerStatus(status=True)

def test_model(client):
    response = client.post(configuration.server.routes.model, data={'question': 'test'})
    assert response.status_code == 200

    llm_response = LLMResponse.model_validate(response.json())

    assert llm_response == LLMResponse(answer="Kein Transformer ist online.", prompt_history="Kein Transformer ist online.\n")
