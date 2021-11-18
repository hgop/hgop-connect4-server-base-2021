# Setup

## CircleCI

### Environment Variables

- DATABASE_USERNAME: your database username
- DATABASE_PASSWORD: your database password
- DOCKERHUB_USERNAME: your docker hub username
- DOCKERHUB_PASS: your docker hub password
- KUBECONFIG_DATA: your kubeconfig base64 encoded
- SECRET_KEY: a random string

## Create virtual python environment

Create a virtual python environment using venv, if you are using VSCode with the python extension
there should be a pop up asking you if you want to select this new venv as your environment. If you
do VSCode will source activation file automatically for each new terminal within VSCode.

~~~bash
python -m venv .venv
source .venv/bin/activate # Skip if using VSCode with extension, open new integrated terminal in VSCode.
pip install -r requirements.txt
pip install -r requirements_dev.txt
~~~

## Linting

You can use the following command to typecheck your code if you are using types (Recommended).

~~~bash
just mypy
~~~

## Start Server

You can start the server locally using docker-compose:

(build flag is so that the game-server is rebuilt incase there are file changes since you last started it)

~~~bash
docker-compose up --build
~~~

You can start up the game-client now with `API_URL=http://localhost:5000` and it should connect with your
local server.

If break your local database while developing, you can remove it using:

~~~bash
docker-compose down
~~~

Start the game-server up again and it should be using a fresh database.
