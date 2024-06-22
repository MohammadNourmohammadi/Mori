FROM python:3.9-slim

RUN apt-get update && apt-get install -y git
RUN pip install --upgrade pip

WORKDIR /app
COPY ./backend/requirements.txt /app
RUN pip install -r requirements.txt

COPY ./backend/src /app

CMD ["python", "main.py"]