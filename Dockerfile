# Base Image
FROM python:3.6-slim as base

# set working directory
WORKDIR /usr/src/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Install system dependencies
RUN apt-get update && apt-get install gcc build-essential libpq-dev -y && \
    python3 -m pip install --no-cache-dir pip-tools

# Clean the house
RUN apt-get purge libpq-dev -y && apt-get autoremove -y && \
    rm /var/lib/apt/lists/* rm -rf /var/cache/apt/*

# install environment dependencies
RUN pip3 install --upgrade pip
RUN pip3 install psycopg2


# Install project dependencies
COPY ./requirements.txt /usr/src/requirements.txt
COPY ./requirements-dev.txt /usr/src/requirements-dev.txt

RUN pip3 install -r requirements.txt && pip3 install -r requirements-dev.txt
# copy project to working dir
COPY . /usr/src/

CMD gunicorn geninfo.wsgi:application --log-file --bind 0.0.0.0:$PORT --reload