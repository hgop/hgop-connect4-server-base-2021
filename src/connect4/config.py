import os

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))

DEBUG = bool(os.getenv("DEBUG", "True"))
TESTING = bool(os.getenv("TESTING", "True"))

DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "postgres")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")
DATABASE_NAME = os.getenv("DATABASE_NAME", "connect4")
DATABASE_HOST = os.getenv("DATABASE_HOST", "connect4-database")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

SECRET_KEY = os.getenv("SECRET_KEY", "this-really-needs-to-be-changed")
