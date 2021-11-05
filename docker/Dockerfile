FROM python:3.10

RUN apt update
RUN apt install vim -y

RUN python -m pip install --upgrade pip

COPY requirements/ /tmp/requirements/

RUN python -m pip install -r /tmp/requirements/base.txt
