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
    question = data.get('question', "")
    context = data.get('context', None)
    logger.info("received question: " + question)
    if context:
        logger.info("received context: " + context)

    prompt_format = "<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    start_time = time.perf_counter()
    result = generator(prompt_format.format(prompt=question), do_sample=True, top_p=0.95, max_length=8192) 
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
