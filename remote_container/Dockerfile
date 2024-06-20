FROM python:3.12.3

WORKDIR /root/workspace

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./remote_container/requirements.txt .

RUN apt-get update && apt-get install -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt

EXPOSE 8000

COPY /src .