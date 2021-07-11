FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE Sprint.settings
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

EXPOSE 8000
