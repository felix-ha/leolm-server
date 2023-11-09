import os
from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
import time
import logging
from config import configuration
from model_api import ServerStatus, LLMResponse
from logic import OfflineModel

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
#file_handler = logging.FileHandler("log.txt")
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

deploy_llm = os.getenv('DEPLOY_LLM', None)
logger.info(f"DEPLOY_LLM: {deploy_llm}")
try:
    logger.info("starting server")
    if deploy_llm:
        logging.info("loading model")
        start_time = time.perf_counter()
        from llm_models import LeoLM
        model = LeoLM()
        end_time = time.perf_counter()
        logger.info("loaded model in " + str(end_time - start_time) + " seconds")
    else: 
        logging.info("using mock model")
        model = OfflineModel()
except Exception as e:
    logger.exception(str(e))
    exit(1)

  
app = FastAPI()


@app.get(configuration.server.routes.status, response_model=ServerStatus)
def server_is_online():
    logger.info("checked server status")
    return ServerStatus(status=True) 


@app.post(configuration.server.routes.model, response_model=LLMResponse)
# TODO input argument as pydantic model 
def ask_model(question: str = Form(...), prompt_history: str = Form(None), rag_context: str = Form(None)) -> LLMResponse:
    logger.info(f'received new chat message')
    try:
        logger.info(f'question: {question}')
        llm_response = model(question, prompt_history)
        logger.info(llm_response)
        return llm_response
    
    except Exception as e:
        logger.exception(str(e))
        return {'error': str(e)}, 400


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=configuration.server.port)
    logger.info("server stopped")
