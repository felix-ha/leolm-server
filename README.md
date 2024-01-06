# transformers-playground

> A python webserver with a streamlit app to provide interactive access to LLMs and quickly test ideas.

Access the app here: https://transformers-playground.felix-jobson.net

The server is offline most of the time due to costs of running it. To start a new chat, the page needs to be refreshed. 

# Features

* Plain chat with a LLM
* Retrieval Augmented Generation (RAG) to ask questions to documents

# Tech stack

* Backend built on top of a [paperspace machine.](https://www.paperspace.com/machines)
* Python webserver is written with [FastAPI](https://github.com/tiangolo/fastapi) and runs in a Docker container with compose.
* Frontend is a [streamlit](https://github.com/streamlit/streamlit) app hosted on the [streamlit community cloud](https://share.streamlit.io/) and talks to the web server via http requests.
* LLMs are deployed with [huggingface transformers.](https://github.com/huggingface/transformers)
* RAG is implemented with [langchain](https://github.com/langchain-ai/langchain) and [faiss.](https://github.com/facebookresearch/faiss)

# Results of RAG 


| Question | Document | Answer | Correct |
| --- | --- | --- | --- |
| Wie lange dauert der erste Studienabschnitt? | [Prüfungsordnung OTH Regensburg](https://www.oth-regensburg.de/fileadmin/Bereiche/Organisation/Rechtliche_Grundlagen/Satzungen_Ordnungen/2013/MaBA_konsolidiert_2013.pdf) | Der erste Studienabschnitt dauert zwei Semester, gemäß § 3 Abs. 1 der Studien- und Prüfungsordnung für den Bachelorstudiengang Mathematik an der Hochschule für angewandte Wissenschaften Regensburg. | ✅ |
| Wann wird man exmatrikutliert? | [Prüfungsordnung OTH Regensburg](https://www.oth-regensburg.de/fileadmin/Bereiche/Organisation/Rechtliche_Grundlagen/Satzungen_Ordnungen/2013/MaBA_konsolidiert_2013.pdf) | Exmatrikulation bezieht sich auf den Prozess, bei dem eine Person offiziell von einer Schule, einem Programm oder einer Einrichtung ausgeschlossen wird. Der Zeitpunkt der Exmatrikulation hängt von den spezifischen Regeln und Vorschriften der Institution ab. An den meisten Hochschulen und Universitäten erfolgt die Exmatrikulation automatisch, sobald der Student alle erforderlichen Kurse absolviert hat, alle angebotenen akademischen Chancen ausgeschöpft hat und alle Verpflichtungen gegenüber der Institution erfüllt hat. In einigen Fällen kann eine Person auch auf eigenen Wunsch exmatrikuliert werden. Es ist erwähnenswert, dass die Exmatrikulation kein permanenter Ausschluss ist, da eine Person nach einer bestimmten Zeit wieder aufgenommen werden kann oder sogar die Möglichkeit hat, wieder in das Programm zurückzukehren. | ❌ info was not in document, answer was generic |
| Was war 2021 in Kanada?| [tageschau.de Artikel über den Klimawandel](https://www.tagesschau.de/wissen/klima/attributionsforschung-100.html) | Eine Hitzewelle brachte Temperaturen von bis zu 49,6 Grad Celsius. | ✅ |
| Was erkannte Henri Poincaré 1895? | [Spektrum der Wissenschaft Artikel über den Kategorientheorie](https://www.spektrum.de/news/kategorientheorie-mathematik-aus-der-vogelperspektive/2197350) |  Henri Poincaré erkannte 1895, dass es eine Möglichkeit gibt, Löcher auf einer geometrischen Form mit algebraischen Mitteln aufzuspüren. Er erkannte, dass eine Möglichkeit darin besteht, alle möglichen geschlossenen Kurven auf einer Oberfläche zu untersuchen. | ✅ |
| Wie oft wurde das Album Back in Black verkauft? | [Wikipedia Artikel über AC/DC](https://de.wikipedia.org/wiki/AC/DC) |  Back in Black hat laut einigen Quellen[2][3][4] über 50 Millionen Tonträger weltweit verkauft. | ✅ |

## ToDos

* Improve RAG parameters, they are not really optimized at the moment. 
* Investigate behaviour of vector database


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




