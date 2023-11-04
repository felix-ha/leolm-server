import argparse
from flask import Flask, request, jsonify
import time
import logging
import tempfile
from pathlib import Path
from index import get_context, get_documents

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

promt_new_question = "<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n" 


def mock_pipeline(*args, **kwargs):
        generated_text = '<|im_start|>assistant\nDebug Modus!'
        return [{'generated_text': generated_text}]


@app.route(route_check)
def server_is_online():
    logger.info("checked server status")
    return "online"


@app.route(route_model, methods=['POST'])
def upload():
    logger.info(f'received new chat message')
    logger.info(f'{request.form=}')
    logger.info(f'{request.form.keys()=}')
    try:

        context_from_file = None
        # TODO remove context, it is not used
        context = None
        # if 'context' in request.form.keys():
        #     context = request.form['context']
        #     logger.info(f'context {context}')
        # else:
        #     context = None
        #     logger.info(f'no context received')

        if 'question' in request.form.keys():
            question = request.form['question']
            logger.info(f'question {question}')
        else:
            question = None
            logger.info(f'no question received')

        if 'prompt' in request.form.keys():
            prompt = request.form['prompt']
            logger.info("prompt history received, continuing conversation")
            prompt = prompt + "<|im_end|>\n" + promt_new_question
        else:
            prompt = promt_new_question
            logger.info("no prompt history received, starting new conversation")

            if request.files:
                with tempfile.TemporaryDirectory() as tmpdir:
                    file = request.files['file']
                    file_path = Path(tmpdir) / file.filename
                    logger.info(f'received file {file.filename}')
                    
                    if file.filename.endswith('.txt'):
                        logger.info(f'processing text file')
                        file.save(file_path)
                        documents = get_documents(str(file_path), chunk_size=250, chunk_overlap=25)
                        context_from_file = get_context(documents, question, n_results=3)
                        context_from_file = "\n\n".join(context_from_file)

                    elif file.filename.endswith('.pdf'):
                        logger.info(f'processing pdf file not implemented yet, continuing without context')
                    else:
                        logger.info(f'not valid file extension, continuing without context')

        if context_from_file:
            logging.info(f'context from file {context_from_file}')
            promt_new_question_with_context = "<|im_start|>user\nMit dieser Information:\n{context}\nBeantworte diese Frage:\n{question}<|im_end|>\n<|im_start|>assistant\n"
            input_prompt = promt_new_question_with_context.format(context=context_from_file, question=question)
            logging.info(f'input prompt {input_prompt}')
        else:
            input_prompt = prompt.format(question=question)

        start_time = time.perf_counter()
        result = generator(input_prompt, do_sample=True, top_p=0.95, max_length=8192) 
        end_time = time.perf_counter()

        response = {'answer': result, 'context': context_from_file, 'inference_time_seconds': end_time - start_time}
        logger.info("response: " + str(response))
        return jsonify(response)
    
    except Exception as e:
        logger.exception(str(e))
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--deploy_llm",
    #     action=argparse.BooleanOptionalAction,
    #     default=False,
    #     help="Load llm, gpu required",
    # )

    # args = parser.parse_args()
    deploy_llm = True
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
            generator = mock_pipeline
    except Exception as e:
        logger.exception(str(e))
        exit(1)
    app.run(host="0.0.0.0", port=port)
    logger.info("server stopped")
