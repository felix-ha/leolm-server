from __future__ import annotations

from pydantic import BaseModel


class Routes(BaseModel):
    status: str
    model: str


class Server(BaseModel):
    port: int
    routes: Routes


class Mock(BaseModel):
    name: str


class Leolm(BaseModel):
    name: str


class Llama2(BaseModel):
    name: str


class Models(BaseModel):
    mock: Mock
    leolm: Leolm
    llama2: Llama2


class Model(BaseModel):
    server: Server
    models: Models
