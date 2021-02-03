FROM python:3.9.1-alpine

WORKDIR /home/unyte

COPY unyte_generator ./unyte_generator
COPY main.py main.py
COPY resources/message.json resources/message.json
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


# RUN python3 main.py -n 10 -t json -i 5 -a 1000 -d headers -l 0.4 192.168.42.1 192.168.0.17 8080 8081
