FROM python:3.10.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install netcat &&  apt-get -y install gettext

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN pip install --upgrade pip && \ 
    pip install -r /code/requirements.txt && \
    chmod +x /code/entrypoint.sh && \
    touch /code/logs/celery.log && \
    chmod +x /code/logs/celery.log

ENTRYPOINT ["/code/entrypoint.sh"]