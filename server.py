import os
from flask import Flask, request, jsonify
import time
import logging
import tempfile
from pathlib import Path
from index import get_context, get_documents
from models.blip2 import run 
from logic import ask_question

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
#file_handler = logging.FileHandler("log.txt")
file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


app = Flask(__name__)

port = 5000
route_check = '/up-status'
route_model = '/llm'
route_upload = '/upload'
route_blip2 = '/blip2'


@app.route(route_blip2, methods=['POST'])
def blip2():
    try:
        result = run()
        response = {'answer': result}
        logger.info("response: " + str(response))
        return jsonify(response)
    except Exception as e:
        logger.exception(str(e))
        return jsonify({'error': str(e)}), 400


@app.route(route_check)
def server_is_online():
    logger.info("checked server status")
    return "online"


@app.route(route_model, methods=['POST'])
def upload():
    logger.info(f'received new chat message')
    try:
        question = request.form['question']
        logger.info(f'question: {question}')

        try:
            prompt = request.form['prompt']
            logger.info(f'prompt: {prompt}')
        except:
            prompt = None
            logger.info(f'no prompt received')
            
        response = ask_question(question, prompt)
        logger.info(response)
        return jsonify(response), 200
    
    except Exception as e:
        logger.exception(str(e))
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
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
    except Exception as e:
        logger.exception(str(e))
        exit(1)
    app.run(host="0.0.0.0", port=port)
    logger.info("server stopped")
