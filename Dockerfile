FROM python:3.10

RUN apt update
RUN apt install vim -y

RUN python -m pip install --upgrade pip

COPY requirements/ /tmp/requirements/
WORKDIR /usr/app

RUN python -m pip install -r /tmp/requirements/base.txt
ENV FLASK_APP microblog.py

EXPOSE 5000
COPY microblog/ /usr/app
CMD ["python", "-m", "app"]