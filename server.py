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
route_mock_model = '/mock-llm'


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

@app.route(route_mock_model, methods=['POST'])
def llm():
    data = request.get_json()
    question = data.get('question', "")
    context = data.get('context', None)
    logger.info("received question: " + question)
    if context:
        logger.info("received context: " + context)

    start_time = time.perf_counter()
    result = mock_model(question, context)   
    end_time = time.perf_counter()

    response = {'answer': result, 'inference_time_seconds': end_time - start_time}
    logger.info("response: " + str(response))
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
