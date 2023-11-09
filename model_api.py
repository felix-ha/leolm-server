from pydantic import BaseModel


class ServerStatus(BaseModel):
    status: bool


class LLMResponseCreate(BaseModel):
    answer: str
    prompt_history: str
    rag_context: str

class LLMResponse(BaseModel):
    answer: str
    prompt_history: str