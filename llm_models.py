

from transformers import pipeline
import torch  
from pydantic import BaseModel
from model_api import LLMResponse


class LeoLM():
    def __init__(self):
        self.name = "LeoLM/leo-mistral-hessianai-7b-chat"
        self.promt_new_question = "<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n" 
        self.promt_new_question_with_context = "<|im_start|>user\nMit dieser Information:\n{rag_context}\nBeantworte diese Frage:\n{question}<|im_end|>\n<|im_start|>assistant\n"
        self.promt_end_message =  "<|im_end|>\n"
        self.do_sample = True
        self.top_p = 0.95
        self.max_length = 8192
        
        self.generator = pipeline(model=self.name, device="cuda", torch_dtype=torch.float16)
        
    def __call__(self, question: str, prompt_history: str=None, rag_context: str=None) -> LLMResponse:
        return self.inference(question, prompt_history, rag_context)
        
    def inference(self, question: str, prompt_history: str=None, rag_context: str=None) -> LLMResponse:
        if prompt_history:
            prompt = prompt_history + self.promt_end_message  + self.promt_new_question
            input_prompt = prompt.format(question=question)
        else:
            input_prompt = self.promt_new_question.format(question=question)
            
            if rag_context:
                input_prompt = self.promt_new_question_with_context.format(rag_context=rag_context, question=question)
                
        output = self.generator(input_prompt, do_sample= self.do_sample, top_p = self.top_p, max_length=self.max_length)
        prompt_history_updated = output[0]['generated_text']
        answer = prompt_history_updated.split('<|im_start|>assistant')[-1].lstrip()
        
        return LLMResponse(answer=answer, prompt_history=prompt_history_updated)
        