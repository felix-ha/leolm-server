from model_config import Model
from pydantic_yaml import parse_yaml_raw_as

with open("config.yaml") as f:
    yml = f.read()

configuration = parse_yaml_raw_as(Model, yml)
