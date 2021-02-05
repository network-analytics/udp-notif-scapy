# Docker container for Scapy

Docker container for the UDP-notif scapy project.

## Build and run 
You can use both `docker` and `podman` engines.

| Commands/scripts                     | Description             |
| ------------------------------------ |-------------------------|
| `./build-docker.sh <docker_engine>`  | Build container for current scapy code. `<docker_engine>` can be `docker` or `podman`. Default: `docker`. |
| `./run-docker.sh <docker_engine>`    | Running container with multiple instances, see the script and adapt as needed. `<docker_engine>` can be `docker` or `podman`. Default: `docker`. |
| `docker ps`                          | See active containers |
| `./stop-docker.sh <docker_engine>`   | Stopping all active scapy containers. `<docker_engine>` can be `docker` or `podman`. Default: `docker`. |
| `docker logs <container_id> -f`      | See a scapy container logs. By default, the logs are binded by a volume in the folder `logs` |


To simply launch one instance of the scapy in a container :
- `docker run unyte/scapy:latest python3 src/main.py <args>` : being `<args>` the arguments showed in the main [README](../README.md#usage) 
