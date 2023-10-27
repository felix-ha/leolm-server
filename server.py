from transformers import pipeline
import torch

from flask import Flask, request, jsonify
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(module)s %(levelname)s - %(message)s")
file_handler = logging.FileHandler("log.txt")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


app = Flask(__name__)

port = 5000
route_check = '/up-status'
route_model = '/llm'

promt_new_question = "<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n" 


def mock_model(question, context):
    if question == "":
        return "Es wurde keine Frage gestellt."
    if context:
        return "Das ist die Antwort mit Kontext!"
    return "Das ist die Antwort ohne Kontext!"

@app.route(route_check)
def server_is_online():
    logger.info("checked server status")
    return "online"

@app.route(route_model, methods=['POST'])
def llm():
    data = request.get_json()
    # context = data.get('context', None)

    question = data.get('question', "")
    prompt = data.get('prompt', None)

    if prompt:
        logger.info("prompt history received, continuing conversation")
        prompt = prompt + "<|im_end|>\n" + promt_new_question
    else:
        logger.info("no prompt history received, starting new conversation")
        prompt = promt_new_question

    # if context:
    #     logger.info("received context: " + context)

    logger.info("received question: " + question)


    start_time = time.perf_counter()
    result = generator(prompt.format(question=question), do_sample=True, top_p=0.95, max_length=8192) 
    end_time = time.perf_counter()

    response = {'answer': result, 'inference_time_seconds': end_time - start_time}
    logger.info("response: " + str(response))
    return jsonify(response)


if __name__ == '__main__':
    logger.info("starting server")
    logging.info("loading model")
    start_time = time.perf_counter()
    generator = pipeline(model="LeoLM/leo-mistral-hessianai-7b-chat", device="cuda", torch_dtype=torch.float16)
    end_time = time.perf_counter()
    logger.info("loaded model in " + str(end_time - start_time) + " seconds")
    app.run(host="0.0.0.0", port=port)
    logger.info("server stopped")
