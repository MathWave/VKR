FROM docker:dind

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg
RUN pip3 install --no-cache --upgrade pip setuptools
RUN addgroup -S docker

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

RUN pip install requests

COPY . /usr/src/app/

CMD ["python", "main.py"]
