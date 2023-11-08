import time


promt_new_question = "<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n" 


def mock_pipeline(*args, **kwargs):
        generated_text = '<|im_start|>assistant\nDebug Modus!'
        return [{'generated_text': generated_text}]


def ask_question(question: str, prompt: str = None, generator=mock_pipeline):
    context_from_file = None
    # TODO remove context, it is not used
    context = None

    if prompt:
        # logger.info("prompt history received, continuing conversation")
        prompt = prompt + "<|im_end|>\n" + promt_new_question
    else:
        prompt = promt_new_question
        # logger.info("no prompt history received, starting new conversation")

        # if request.files:
        #     with tempfile.TemporaryDirectory() as tmpdir:
        #         file = request.files['file']
        #         file_path = Path(tmpdir) / file.filename
        #         logger.info(f'received file {file.filename}')
                
        #         if file.filename.endswith('.txt'):
        #             logger.info(f'processing text file')
        #             file.save(file_path)
        #             documents = get_documents(str(file_path), chunk_size=250, chunk_overlap=25)
        #             context_from_file = get_context(documents, question, n_results=3)
        #             context_from_file = "\n\n".join(context_from_file)

        #         elif file.filename.endswith('.pdf'):
        #             logger.info(f'processing pdf file not implemented yet, continuing without context')
        #         else:
        #             logger.info(f'not valid file extension, continuing without context')



    if context_from_file:
        # logging.info(f'context from file {context_from_file}')
        promt_new_question_with_context = "<|im_start|>user\nMit dieser Information:\n{context}\nBeantworte diese Frage:\n{question}<|im_end|>\n<|im_start|>assistant\n"
        input_prompt = promt_new_question_with_context.format(context=context_from_file, question=question)
        # logging.info(f'input prompt {input_prompt}')
    else:
        input_prompt = prompt.format(question=question)

    start_time = time.perf_counter()
    result = generator(input_prompt, do_sample=True, top_p=0.95, max_length=8192) 
    end_time = time.perf_counter()

    response = {'answer': result, 'context': context_from_file, 'inference_time_seconds': end_time - start_time}
    return response
