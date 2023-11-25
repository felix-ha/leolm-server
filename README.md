# transformers-playground

> A python webserver with a streamlit app to provide interactive access to LLMs and quickly test ideas.

Access the app here: https://transformers-playground.streamlit.app/

# Features

* Plain chat with a LLM
* Retrieval Augmented Generation (RAG) to ask questions to documents

# Tech stack

* Backend built on top of a [paperspace machine.](https://www.paperspace.com/machines)
* Python webserver is written with [FastAPI](https://github.com/tiangolo/fastapi) and runs in a Docker container with compose.
* Frontend is a [streamlit](https://github.com/streamlit/streamlit) app hosted on the [streamlit community cloud](https://share.streamlit.io/) and talks to the web server via http requests.
* LLMs are deployed with [huggingface transformers.](https://github.com/huggingface/transformers)
* RAG is implemented with [langchain](https://github.com/langchain-ai/langchain) and [faiss.](https://github.com/facebookresearch/faiss)

# Start server

Make sure that the [server is configured](https://github.com/felix-ha/transformers-playground#installation-of-server). Run `make build` to build the Docker image. `make run` creates the container with Docker compose, loads the model and starts the server. Then the server also starts automatically when the machine is booted.


# Installation of server

Prerequisite is a fresh [paperspace](https://www.paperspace.com/machines) P5000 ML in a box virtual server. This machine is equipped with a NVIDIA GPU that has 16 GB RAM.

## update and upgrade 
```bash
sudo apt update && sudo apt upgrade -y
```

## Install docker compose

```bash
export DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
```
```bash
mkdir -p $DOCKER_CONFIG/cli-plugins
```
```bash
curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
```
```bash
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```
see also [official docs](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).

use docker without sudo
```bash
sudo usermod -aG docker $USER
```
```bash
newgrp docker
```

## Configure streamlit

Set the `IP_ADRESS_SERVER` environment variable in the [streamlit community cloud](https://share.streamlit.io/) settings as a secret. 




