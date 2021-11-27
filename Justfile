export DATABASE_CONTAINER := "migration_db"
export DATABASE_USERNAME := "postgres"
export DATABASE_PASSWORD := "postgres"
export DATABASE_NAME := "connect4"
export DATABASE_HOST := "localhost"
export DATABASE_PORT := "5432"

venv:
    python3 -m venv --prompt hgop .venv

install:
    pip install -r requirements.txt
    pip install -r requirements_dev.txt

mypy:
    mypy ./src/

start:
	docker-compose down
	docker-compose rm
	docker-compose up --build

add_migration message:
    docker kill "${DATABASE_CONTAINER}" || true
    docker rm "${DATABASE_CONTAINER}" || true
    docker run -d \
        --name="${DATABASE_CONTAINER}" \
        -e POSTGRES_USERNAME="${DATABASE_USERNAME}" \
        -e POSTGRES_PASSWORD="${DATABASE_PASSWORD}" \
        -e POSTGRES_DB="${DATABASE_NAME}" \
        -p "${DATABASE_PORT}:5432" \
        postgres:13-alpine
    sleep 10
    PYTHONPATH=./src FLASK_APP=./src/connect4/app.py flask db migrate -m "{{message}}"
    docker kill "${DATABASE_CONTAINER}" || true
    docker rm "${DATABASE_CONTAINER}" || true
