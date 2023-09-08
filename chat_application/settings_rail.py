from .settings import *
from os import environ


SECRET_KEY = environ.get("SECRET_KEY")

ALLOWED_HOSTS = ["chatapplication-production-e945.up.railway.app", "localhost", "*"]
