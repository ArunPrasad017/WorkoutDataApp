FROM python:3.10

RUN apt update
RUN apt install vim -y

RUN python -m pip install --upgrade pip

COPY requirements/ /tmp/requirements/
COPY src/ /usr/app/src

RUN python -m pip install -r /tmp/requirements/base.txt
WORKDIR /usr/app
EXPOSE 5000