from pydantic import BaseModel
from typing import Optional
from transformers import pipeline, AutoTokenizer
import torch
import os


class Message(BaseModel):
    role: str
    content: str


class Chat(BaseModel):
    messages: Optional[list[Message]] = []

    def add_question(self, question: str):
        self.messages.append(Message(role="user", content=question))

    def add_answer(self, answer: str):
        self.messages.append(Message(role="assistant", content=answer))


class LLMQuestion(BaseModel):
    question: str
    chat: Chat


class LLMResponse(BaseModel):
    answer: str
    chat: Chat


def mock_generator(*args, **kwargs):
    pass


class MockTokenizer:
    def apply_chat_template(*args, **kwargs):
        return ""


class LLM:
    def __init__(self):

        self.generator = mock_generator
        self.tokenizer = MockTokenizer()
        

        self.do_sample = True
        self.top_p = 0.95
        self.max_length = 8192

        self.access_token = os.getenv('HF_ACCESS_TOKEN', default = None)

    def __call__(
        self, question: str, chat: Chat = Chat(), rag_context: str = None
    ) -> LLMResponse:
        if rag_context:
            pass
        return self.continue_chat(question, chat)


    def continue_chat(self, question: str, chat: Chat) -> LLMResponse:
        chat_result = chat.model_copy(deep=True)
        chat_result.add_question(question)

        input_prompt = self.tokenizer.apply_chat_template(
            chat_result, tokenize=False, add_generation_prompt=True
        )
        answer = self.generate_answer(input_prompt)

        chat_result.add_answer(answer)
        return LLMResponse(answer=answer, chat=chat_result)
    
        
    def generate_answer(self, input_prompt: str) -> str:
        return "No Transformer loaded!"


class LLMTransformer(LLM):
    def __init__(self, model_config):
        super().__init__() 
        self.generator = pipeline(model=model_config.name, device="cuda", torch_dtype=torch.float16, token=self.access_token)
        self.tokenizer = AutoTokenizer.from_pretrained(model_config.name, token=self.access_token)
        self.split_string_for_answer = model_config.split_string_for_answer
    
    def generate_answer(self, input_prompt: str) -> str:
        output = self.generator(input_prompt,do_sample=self.do_sample,top_p=self.top_p,max_length=self.max_length,)
        answer = output[0]["generated_text"].split(self.split_string_for_answer)[-1].lstrip()
        return answer

    # TODO: this removes not all memory
    def gc(self):
        del self.generator
        del self.tokenizer
        torch.cuda.empty_cache()
