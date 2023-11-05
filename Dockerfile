FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

RUN apt update
RUN apt install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP=server.py

CMD [ "python3", "server.py"]
