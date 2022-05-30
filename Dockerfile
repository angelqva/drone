FROM python:3.10.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get -y install netcat &&  apt-get -y install gettext


WORKDIR /code
COPY . ./

RUN python -m pip install --upgrade pip
RUN pip install -r /code/requirements.txt
RUN chmod +x /code/entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]