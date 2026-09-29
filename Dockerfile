FROM python:3.9-alpine

ENV FLASK_APP=hello.py

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY hello.py .
COPY templates templates

EXPOSE 5000
ENTRYPOINT ["venv/bin/flask", "run", "--host=0.0.0.0"]