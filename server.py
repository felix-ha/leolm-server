import os
from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
import time
import logging
from logic import ask_question

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
#file_handler = logging.FileHandler("log.txt")
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

deploy_llm = os.getenv('DEPLOY_LLM', None)
deploy_llm = None
logger.info(f"DEPLOY_LLM: {deploy_llm}")
try:
    logger.info("starting server")
    if deploy_llm:
        logging.info("loading model")
        start_time = time.perf_counter()
        from transformers import pipeline
        import torch  
        generator = pipeline(model="LeoLM/leo-mistral-hessianai-7b-chat", device="cuda", torch_dtype=torch.float16)
        end_time = time.perf_counter()
        logger.info("loaded model in " + str(end_time - start_time) + " seconds")
    else: 
        logging.info("using mock model")
        generator = None
except Exception as e:
    logger.exception(str(e))
    exit(1)

  
app = FastAPI()


port = 5000
route_check = '/up-status'
route_model = '/llm'
route_upload = '/upload'


@app.get(route_check)
def server_is_online():
    logger.info("checked server status")
    return "online"


@app.post(route_model)
def upload(question: str = Form(...), prompt: str = Form(None)):
    logger.info(f'received new chat message')
    try:
        logger.info(f'question: {question}')
        response = ask_question(question, prompt, generator)
        logger.info(response)
        return response, 200
    
    except Exception as e:
        logger.exception(str(e))
        return {'error': str(e)}, 400


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port)
    logger.info("server stopped")
