import os
from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
import time
import logging
from config import configuration
from model_api import ServerStatus
from logic import LLM, LLMQuestion, LLMResponse


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
        model = LLM(configuration.models.leo_lm.name)
        end_time = time.perf_counter()
        logger.info("loaded model in " + str(end_time - start_time) + " seconds")
    else: 
        logging.info("using mock model")
        model = LLM(configuration.models.mock.name)
except Exception as e:
    logger.exception(str(e))
    exit(1)

  
app = FastAPI()


@app.get(configuration.server.routes.status, response_model=ServerStatus)
def server_is_online():
    logger.info("checked server status")
    return ServerStatus(status=True) 
   

@app.post(configuration.server.routes.model, response_model=LLMResponse)
def create_item(item: LLMQuestion):
    print(item)
    return model(item.question, item.chat)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=configuration.server.port)
    logger.info("server stopped")
