from fastapi.testclient import TestClient
import tempfile
from typing import List
from pathlib import Path
from server import app
import pytest
from config import configuration
from model_api import ServerStatus
from logic import LLMResponse, LLMQuestion, Chat
from test_logic import expected_llm_response_1, expected_llm_response_2

# TODO fix this handling of files on server
from server import clear_upload_folder


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
    response_1 = client.post(
        configuration.server.routes.model, json=question_1.model_dump()
    )
    llm_response_1 = LLMResponse.model_validate(response_1.json())

    question_2 = LLMQuestion(question="Fine", chat=llm_response_1.chat)
    response_2 = client.post(
        configuration.server.routes.model, json=question_2.model_dump()
    )
    llm_response_2 = LLMResponse.model_validate(response_2.json())

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    assert llm_response_1 == expected_llm_response_1
    assert llm_response_2 == expected_llm_response_2


def test_upload_files(client):
    with tempfile.TemporaryDirectory() as temp_dir:
        # create test .txt files
        file_name_1 = "upload.txt"
        file_path_1 = str(Path(temp_dir) / file_name_1)
        with open(file_path_1, "wb") as buffer:
            buffer.write(b"This is a test file!")

        file_name_2 = "upload_2.txt"
        file_path_2 = str(Path(temp_dir) / file_name_2)
        with open(file_path_2, "wb") as buffer:
            buffer.write(b"This is also a test file!")
        
        # TODO open files with context manager
        files = [('files', open(file_path_1, 'rb')), ('files', open(file_path_2, 'rb'))]

        # send to server
        response = client.post(configuration.server.routes.upload, files=files)
        result = response.json()


    clear_upload_folder()

    assert result == {'file_names': [file_name_1, file_name_2], 'contents': ["This is a test file!", "This is also a test file!"]}


#def test_uploadfile(client):
#    with tempfile.TemporaryDirectory() as temp_dir:

        # create test .txt file
#        file_name = "upload.txt"
#        file_path = str(Path(temp_dir) / file_name)
#        with open(file_path, "wb") as buffer:
#            buffer.write(b"This is a test file!")

        # load file
#        with open(file_path, 'rb') as file:
#            file_upload = {'file': (file_path, file)}

#            response = client.post(configuration.server.routes.rag, files=file_upload)


#    assert response.status_code == 200

#def test_uploadfile(client):
#    with tempfile.TemporaryDirectory() as temp_dir:
#
#        # create test .txt file
#        file_name = "upload.txt"
#        file_path = str(Path(temp_dir) / file_name)
#        with open(file_path, "wb") as buffer:
#            buffer.write(b"This is a test file!")
#
#        # load file
#        with open(file_path, 'rb') as file:
#            files = {'file': (file_path, file)}
#
#            question = LLMQuestion(question="How are you?", chat=Chat())
#
#           # send to server
#            response = client.post(configuration.server.routes.rag, json=question.model_dump(), files=files)
#
#    assert response.status_code == 200
    #llm_response = LLMResponse.model_validate(response.json())

    #assert response.status_code == 200
    #assert llm_response == expected_llm_response_context


