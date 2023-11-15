import os
import tempfile
from typing import List
from pathlib import Path
import shutil
from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
import time
import logging
from config import configuration
from model_api import ServerStatus
from logic import LLM, LLMQuestion, LLMResponse, LLMTransformer
from index import get_documents, get_context


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
# file_handler = logging.FileHandler("log.txt")
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

deploy_llm = os.getenv("DEPLOY_LLM", None)
logger.info(f"DEPLOY_LLM: {deploy_llm}")
try:
    logger.info("starting server")
    if deploy_llm:
        logging.info("loading model")
        start_time = time.perf_counter()
        model = LLMTransformer(configuration.models.leolm)
        end_time = time.perf_counter()
        logger.info("loaded model in " + str(end_time - start_time) + " seconds")
    else:
        logging.info("using mock model")
        model = LLM()
except Exception as e:
    logger.exception(str(e))
    exit(1)


app = FastAPI()


def clear_upload_folder():
    for file_current in os.listdir('resources'):
        file_current_name = Path('resources') / file_current
        if os.path.exists(file_current_name):
            os.remove(file_current_name)


@app.get(configuration.server.routes.status, response_model=ServerStatus)
def server_is_online():
    logger.info("checked server status")
    return ServerStatus(status=True)


@app.post(configuration.server.routes.model, response_model=LLMResponse)
def create_item(item: LLMQuestion):
    context = None
    try: 
        for file_current in os.listdir('resources'):
            file_current_name = Path('resources') / file_current
            model_name = "distiluse-base-multilingual-cased-v1"
            documents = get_documents(str(file_current_name), chunk_size=1000, chunk_overlap=25)
            context = get_context(documents, query, n_results=5, model_name=model_name)
    except Exception as e:
        logger.info('rag failed')
        logger.exception(str(e))
    finally: 
        # always clear upload folder to make sure rag is not performed on next call
        clear_upload_folder()
    return model(item.question, item.chat, context)


#@app.post(configuration.server.routes.rag, response_model=LLMResponse)
#def do_rag(item: LLMQuestion, file: UploadFile = File(...)):
#    with tempfile.TemporaryDirectory() as temp_dir:
#        file_name = Path(temp_dir) / file.filename
#        with open(file_name, "wb") as buffer:
#            shutil.copyfileobj(file.file, buffer)
#
#        file_extension = file_name.suffix
#
#        if file_extension == ".pdf":
#            model_name = "distiluse-base-multilingual-cased-v1"
#            documents = get_documents(str(file_name), chunk_size=1000, chunk_overlap=25)
#            context = get_context(documents, query, n_results=5, model_name=model_name)
#        else:
#            context = "context"
#
#    return model(item.question, item.chat, context)

#@app.post(configuration.server.routes.rag)
#def create_item(UploadFile = File(...)):
#    file_name = Path('resources') / file.filename

    # check if file_name exists and if so delete it 
#    if os.path.exists(file_name):
#        os.remove(file_name)

#    with open(file_name, "wb") as buffer:
#        shutil.copyfileobj(file.file, buffer)

#    app.file = file_name
    


@app.post(configuration.server.routes.upload)
def create_upload_file(files: List[UploadFile] = File(...)):

    file_names = []
    contents = []

    # check if files in folder 'resources' and if so delete them
    clear_upload_folder()


    for file_current in files:
        file_current_name = Path('resources') / file_current.filename
        with open(file_current_name, "wb") as buffer:
            shutil.copyfileobj(file_current.file, buffer)

        with open(file_current_name, "rb") as buffer:
            contents.append(buffer.read())

        file_names.append(file_current.filename)

    return {'file_names': file_names, 'contents': contents}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=configuration.server.port)
    logger.info("server stopped")
