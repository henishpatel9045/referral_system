from .common import *
from decouple import Csv

SECRET_KEY = config("DJANGO_APP_SECRET")

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
