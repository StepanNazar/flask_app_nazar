import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
FLASK_DEBUG = 1