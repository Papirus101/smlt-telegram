FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y python3-dev libpq-dev

COPY requirements.txt .

RUN python3.11 -m pip install -r requirements.txt

COPY . .