# https://hub.docker.com/_/python
FROM python:3.11-slim
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV MODULE server
WORKDIR $APP_HOME

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY __init__.py $APP_HOME/$MODULE
COPY src $APP_HOME/$MODULE/src
COPY certs /certs

CMD python $MODULE/src/app.py