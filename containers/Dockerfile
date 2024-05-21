FROM python:3.12.3

ARG DEBUG
ARG SECRET_KEY

ENV PYTHONUNBUFFERED 1
ENV DEBUG=${DEBUG}
ENV SECRET_KEY=${SECRET_KEY}

RUN mkdir -p /root/workspace
COPY requirements.txt /root/workspace/
WORKDIR /root/workspace

RUN pip install --upgrade pip\
    && pip install --upgrade setuptools\
    && pip install -r requirements.txt