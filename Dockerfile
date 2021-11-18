FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY migrations/ ./migrations/
COPY src/connect4/*.py ./src/connect4/

ENV PYTHONPATH=/app/src/
ENV FLASK_APP=/app/src/connect4/app.py

CMD ["python", "/app/src/connect4/app.py"]
