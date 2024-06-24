FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip

COPY ./backend/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./backend/src /app

CMD ["python", "main.py"]