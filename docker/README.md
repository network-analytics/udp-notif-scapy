# Docker container for Scapy

Docker container for the UDP-notif scapy project.

## Build and run 
- Build: `./build-docker.sh`
- Run container : `./run-container.sh`
- Active dockers: `docker ps`
- Stopping containers : `docker stop <container_id>`
- Logs from container : `docker logs <container_id> -f`

The `run-container.sh` script launch multiple containers simulating UDP-notif messages. You can adapt the script depending your needs.

To simply launch one instance of the scapy in a container :
- `docker run unyte/scapy:latest python3 src/main.py <args>` : being `<args>` the arguments showed in the main [README](../README.md#usage) 

## Notes :

`docker run -itd -p 9340:9340/udp scapy_worker python main.py 192.168.1.10 192.168.1.10 9340 9341 -n 1000 -m 1024 -l 0.02 -r 1`

`CMD [ "python", "./main.py", "192.168.1.10", "192.168.1.10", "9340", "9341", "-n 1000", "-m 1024", "-l 0.02", "-r 1" ]`
