# transformers-playground

## Installation of server

update and upgrade 
```
sudo apt update && sudo apt upgrade -y
```

### Docker

Install [docker compose](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually):

```
export DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
use docker without sudo
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```


```
sudo usermod -aG docker $USER
```

```
newgrp docker
```

## Start server

Run `make build` to build and `make run` to start server.
