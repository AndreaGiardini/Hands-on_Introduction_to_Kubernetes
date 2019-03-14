FROM python:3.6-alpine

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
#ENTRYPOINT ["flask", "run"]
