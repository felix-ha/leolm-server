# transformers-playground

## Installation of server

update and upgrade 
```
sudo apt update && sudo apt upgrade -y
```

### Docker

Install [docker compose](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually)

use docker without sudo

```
sudo usermod -aG docker $USER
```

```
newgrp docker
```

## Start server

Run `make build` to build and `make run` to start server.
