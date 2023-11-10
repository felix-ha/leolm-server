from pydantic import BaseModel
from typing import Optional

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

class MockTockenizer:
    def apply_chat_template(*args, **kwargs):
        return ""


class LLM():
    def __init__(self, name):
        self.name = name
        self.load_model()
        
        self.do_sample = True
        self.top_p = 0.95
        self.max_length = 8192
        
    def __call__(self, question: str,  chat: Chat = Chat(), rag_context: str = None) -> LLMResponse:
        if rag_context:
            pass
        return self.continue_chat(question, chat)

        
    def load_model(self):
        if self.name == "offline":
            self.generator = mock_generator
            self.tokenizer = MockTockenizer
        else:  
            self.generator = self.get_pipeline(self.name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.name)          
        
        
    def continue_chat(self, question: str, chat: Chat) -> LLMResponse:
        chat_result = chat.model_copy(deep=True)
        chat_result.add_question(question)
        
        input_prompt = self.tokenizer.apply_chat_template(chat_result, tokenize=False, add_generation_prompt=True)       
        answer = self.call_hf(input_prompt)
        
        chat_result.add_answer(answer)
        return LLMResponse(answer=answer, chat=chat_result)
    
    
    def get_pipeline(self, name):
        if name == "LeoLM/leo-mistral-hessianai-7b-chat":
            return pipeline(model=self.name, device="cuda", torch_dtype=torch.float16)
        else:
            return mock_generator
        
    
    def call_hf(self, input_prompt: str) -> str:
        if self.name == "offline":
            answer = "No Transformer loaded!"
        elif self.name == "LeoLM/leo-mistral-hessianai-7b-chat":
            output = self.generator(input_prompt, do_sample= self.do_sample, top_p = self.top_p, max_length=self.max_length)
            answer = output[0]['generated_text'].split('<|im_start|>assistant')[-1].lstrip()
        else:
            answer = f"Model {self.name} is not implemented"
        return answer
    
    def gc(self):
        del self.generator
        try:
            torch.cuda.empty_cache()
        except:
            pass
