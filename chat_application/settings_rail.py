from .settings import *
from decouple import config


SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ["chatapplication-production-e945.up.railway.app", "localhost", "*"]
