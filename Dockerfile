FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip

# Install Python 3.11 manually
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.11

RUN ln -s /usr/bin/python3.11 /usr/bin/python3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
