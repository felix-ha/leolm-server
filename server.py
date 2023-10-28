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
route_upload = '/upload'

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

# @app.route(route_model, methods=['POST'])
# def llm():
#     data = request.get_json()
#     # context = data.get('context', None)

#     question = data.get('question', "")
#     prompt = data.get('prompt', None)

#     if prompt:
#         logger.info("prompt history received, continuing conversation")
#         prompt = prompt + "<|im_end|>\n" + promt_new_question
#     else:
#         logger.info("no prompt history received, starting new conversation")
#         prompt = promt_new_question

#     # if context:
#     #     logger.info("received context: " + context)

#     logger.info("received question: " + question)


#     start_time = time.perf_counter()
#     result = generator(prompt.format(question=question), do_sample=True, top_p=0.95, max_length=8192) 
#     end_time = time.perf_counter()

#     response = {'answer': result, 'inference_time_seconds': end_time - start_time}
#     logger.info("response length: " + len(str(response['answer'][0]['generated_text'])))
#     logger.info("response: " + str(response))
#     return jsonify(response)


@app.route(route_model, methods=['POST'])
def upload():
    logger.info(f'received new chat message')
    logger.info(f'{request.form=}')
    logger.info(f'{request.form.keys()=}')
    try:

        # TODO remove context, it is not used
        if 'context' in request.form.keys():
            context = request.form['context']
            logger.info(f'context {context}')
        else:
            context = None
            logger.info(f'no context received')

        if 'question' in request.form.keys():
            question = request.form['question']
            logger.info(f'question {question}')
        else:
            question = None
            logger.info(f'no question received')

        if 'prompt' in request.form.keys():
            promt_new_question = request.form['prompt']
            logger.info("prompt history received, continuing conversation")
            prompt = prompt + "<|im_end|>\n" + promt_new_question
        else:
            prompt = promt_new_question
            logger.info("no prompt history received, starting new conversation")

            if request.files:
                file = request.files['file']
                logger.info(f'received file {file.filename}')
                
                if file.filename.endswith('.txt'):
                    logger.info(f'processing text file')
                    pass
                elif file.filename.endswith('.pdf'):
                    logger.info(f'processing pdf file')
                else:
                    pass


        logger.info("received question: " + question)

        start_time = time.perf_counter()
        result = generator(prompt.format(question=question), do_sample=True, top_p=0.95, max_length=8192) 
        end_time = time.perf_counter()

        response = {'answer': result, 'inference_time_seconds': end_time - start_time}
        logger.info("response length: " + len(str(response['answer'][0]['generated_text'])))
        logger.info("response: " + str(response))
        return jsonify(response)
    
    except Exception as e:
        logger.info(str(e))
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    logger.info("starting server")
    logging.info("loading model")
    start_time = time.perf_counter()
    generator = pipeline(model="LeoLM/leo-mistral-hessianai-7b-chat", device="cuda", torch_dtype=torch.float16)
    end_time = time.perf_counter()
    logger.info("loaded model in " + str(end_time - start_time) + " seconds")
    app.run(host="0.0.0.0", port=port)
    logger.info("server stopped")
