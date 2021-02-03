# Docker container for Scapy

## Build and run 
- Build: `./build-docker.sh`
- Run container : `./run-container.sh`
- Active dockers: `docker ps`
- Stopping containers : `docker stop <container_id>`
- Logs from container : `docker logs <container_id> -f`

## Docker notes :

`docker run -itd -p 9340:9340/udp scapy_worker python main.py 192.168.1.10 192.168.1.10 9340 9341 -n 1000 -m 1024 -l 0.02 -r 1`

`CMD [ "python", "./main.py", "192.168.1.10", "192.168.1.10", "9340", "9341", "-n 1000", "-m 1024", "-l 0.02", "-r 1" ]`
