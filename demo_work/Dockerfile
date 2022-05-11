FROM python:3.10.0-slim

WORKDIR /usr/src/Market

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "migrate", "--noinput" ]
CMD [ "python", "manage.py", "loaddata", "fixtures/fixture.json"]