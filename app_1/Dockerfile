FROM python:3.9-slim

WORKDIR /app_1

COPY . .

RUN pip install -r requirements.txt 

CMD gunicorn --bind 0.0.0.0:5000 index:app

