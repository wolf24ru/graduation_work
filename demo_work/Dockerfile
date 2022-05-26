FROM python:3.10.0-slim

WORKDIR /usr/src/Market

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get autoremove --yes \
    && apt-get autoclean

CMD [ "python", "manage.py", "migrate", "--noinput" ]
CMD [ "python", "manage.py", "loaddata", "fixtures/fixture.json"]
CMD [ "python", "manage.py", "spectacular", "--file", "schema.yml"]
CMD [ "python", "manage.py", "collectstatic"]