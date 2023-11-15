from __future__ import annotations

from pydantic import BaseModel


class Routes(BaseModel):
    status: str
    model: str
    upload: str


class Server(BaseModel):
    port: int
    routes: Routes


class Leolm(BaseModel):
    name: str
    split_string_for_answer: str


class Llama2(BaseModel):
    name: str
    split_string_for_answer: str


class Models(BaseModel):
    leolm: Leolm
    llama2: Llama2


class Model(BaseModel):
    server: Server
    models: Models
