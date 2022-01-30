import os

PROTOCOL = os.environ.get("PROTOCOL")

API_HOST = os.environ.get("API_HOST")
API_PORT = os.environ.get("API_PORT")

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

APP_SECRET_KEY = os.environ.get("APP_SECRET_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_URL = f"{PROTOCOL}{API_HOST}:{API_PORT}"
ROOT_URL = f"{PROTOCOL}{HOST}:{PORT}"
OK_CODES = (200,201,202,203,204,205)