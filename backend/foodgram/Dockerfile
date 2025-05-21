FROM python:3.10-slim

RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y libpq-dev gcc netcat-traditional

WORKDIR /app

COPY requirements.txt ./
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir

COPY . ./

CMD ["python", "manage.py", "runserver", "0:8000"] 