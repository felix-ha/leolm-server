from fastapi.testclient import TestClient
from server import app  
import pytest
from config import configuration
from model_api import ServerStatus
from logic import LLMResponse, LLMQuestion, Chat 
from test_logic import expected_llm_response_1, expected_llm_response_2


@pytest.fixture
def client():
    return TestClient(app)


def test_status(client):
    response = client.get(configuration.server.routes.status)
    server_status = ServerStatus.model_validate(response.json())
    assert response.status_code == 200
    assert server_status == ServerStatus(status=True)


def test_start_chat(client):
    # TODO: fix need to instantiate empty chat
    question_1 = LLMQuestion(question="How are you?", chat=Chat())
    response_1 = client.post(configuration.server.routes.model, json=question_1.model_dump())
    llm_response_1 = LLMResponse.model_validate(response_1.json())

    question_2 = LLMQuestion(question="Fine", chat=llm_response_1.chat)
    response_2 = client.post(configuration.server.routes.model, json=question_2.model_dump())
    llm_response_2 = LLMResponse.model_validate(response_2.json())
    
    assert response_1.status_code == 200
    assert response_2.status_code == 200

    assert llm_response_1 == expected_llm_response_1
    assert llm_response_2 == expected_llm_response_2
 