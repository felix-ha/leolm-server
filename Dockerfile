FROM python:3.10-slim-buster

ENV HUGGINGFACE_HUB_CACHE=/tmp/huggingface_hub

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=server.py

CMD [ "python3", "server.py", "--deploy_llm"]