import time
from model_api import LLMResponse


class OfflineModel():
    def __init__(self):
        self.name = "offline-model"
        
    def __call__(self, question: str,  prompt_history: str = None, rag_context: str = None) -> LLMResponse:
        return self.inference(question, prompt_history, rag_context)
        
    def inference(self, question: str, prompt_history: str, rag_context: str) -> LLMResponse:
        if prompt_history:
            answer = "Transformer ist immer noch nicht online."
            prompt_history = prompt_history + "\n" + answer
        else:
            answer = "Kein Transformer ist online."
            prompt_history = answer + "\n"
            
            if rag_context:
                answer = "Kein Transformer ist online um die Frage zum Dokument zu beantworten."
        
        return LLMResponse(answer=answer, prompt_history=prompt_history)
