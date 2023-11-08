FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu20.04

RUN apt update
RUN apt install -y python3 python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
