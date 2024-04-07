FROM python:3.12

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install supervisor -y

WORKDIR /home/app

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY codeRunner.conf /etc/supervisor/conf.d/
COPY . .