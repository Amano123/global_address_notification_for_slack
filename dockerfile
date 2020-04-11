FROM python:latest

RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install requests
ADD ./cron /app/cron/
ADD ./ /app/