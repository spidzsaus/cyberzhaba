FROM python:3.10

WORKDIR /app

COPY . .

RUN py -m pip install -r requirements.txt

RUN py main.py