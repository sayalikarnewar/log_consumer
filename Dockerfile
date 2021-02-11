FROM python:3.7

RUN apt-get update
RUN pip3 install pika
RUN pip3 install pymongo