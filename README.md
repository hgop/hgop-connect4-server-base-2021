# Setup

## Create virtual python environment

Create a virtual python environment using venv, if you are using VSCode with the python extension
there should be a pop up asking you if you want to select this new venv as your environment. If you
do VSCode will source activation file automatically for each new terminal within VSCode.

~~~bash
just venv
source .venv/bin/activate # Skip if using VSCode with extension, open new integrated terminal in VSCode.
just install
~~~

## Linting

You can use the following command to typecheck your code if you are using types (Recommended).

~~~bash
just mypy
~~~

## Start Server

~~~bash
just start
~~~
