apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
python3 -m ensurepip
apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg
pip3 install --no-cache --upgrade pip setuptools
pip3 install -r requirements.txt
python3 manage.py receive