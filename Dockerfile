FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY migrations/ ./migrations/
COPY src/connect4/*.py ./src/connect4/

ENV PYTHONPATH=/app/src/

CMD [python ./src/connect4/app.py]
