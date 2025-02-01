FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev net-tools curl

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "test_runner.wsgi:application"]
