FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 7755

ENV FLASK_APP core/server.py

CMD ["gunicorn", "-c", "gunicorn_config.py", "core.server:app"]
