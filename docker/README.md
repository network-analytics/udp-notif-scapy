# Docker container for scapy

## Docker barbaric commands :

`docker run -itd -p 9340:9340/udp scapy_worker python main.py 192.168.1.10 192.168.1.10 9340 9341 -n 1000 -m 1024 -l 0.02 -r 1`

`CMD [ "python", "./main.py", "192.168.1.10", "192.168.1.10", "9340", "9341", "-n 1000", "-m 1024", "-l 0.02", "-r 1" ]`

## Useful links
- [How to use docker-compose](https://pspdfkit.com/blog/2018/how-to-use-docker-compose-to-run-multiple-instances-of-a-service-in-development/)
