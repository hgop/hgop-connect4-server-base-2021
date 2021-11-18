venv:
    python3 -m venv --prompt hgop .venv

install:
    pip install -r requirements.txt
    pip install -r requirements_dev.txt

mypy:
    mypy ./src/connect4/

pylint:
    pylint ./src/connect4/
