FROM python:3.9-slim-buster

COPY requirements.txt /
RUN groupadd -g 1005 app && useradd -u 205 -g 1005 app
RUN pip install -qU pip && pip install -r requirements.txt
USER app
