FROM python:3

WORKDIR .

RUN pip install --pre scapy[basic]

COPY . .