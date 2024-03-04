FROM python:3.10.12
COPY src/config /usr/src/config
COPY src/controller /usr/src/controller
COPY src/loader /usr/src/loader
COPY src/sink /usr/src/sink
COPY src/transformation /usr/src/transformation
COPY src/logger /usr/src/logger
COPY src/main.py /usr/src/
COPY src/resources /usr/src/resources
COPY Makefile /usr/src/
COPY requirements.txt /usr/src/
RUN pip install -r /usr/src/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/usr/src"
WORKDIR /usr/src