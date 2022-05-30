FROM python:3.10.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install netcat &&  apt-get -y install gettext


WORKDIR /code
COPY . ./

RUN pip install -r /code/requirements.txt 
RUN chmod +x /code/entrypoint.sh
RUN touch /code/logs/celery.log

ENTRYPOINT ["/code/entrypoint.sh"]