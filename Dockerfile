FROM python:alpine3.7

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py server.py ./

ARG OPEN_WEATHER_API_KEY
EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:$PORT server:app