FROM docker:dind

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg
RUN pip3 install --no-cache --upgrade pip setuptools
RUN addgroup -S docker

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE Sprint.settings
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r requirements.txt

EXPOSE 8000
