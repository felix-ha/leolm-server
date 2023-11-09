# generated by datamodel-codegen:
#   filename:  config.yaml
#   timestamp: 2023-11-09T20:27:35+00:00

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


class Models(BaseModel):
    mock: Mock
    leolm: Leolm


class Model(BaseModel):
    server: Server
    models: Models