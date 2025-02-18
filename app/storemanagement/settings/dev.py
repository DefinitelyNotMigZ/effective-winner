from .base import *
from datetime import timedelta

INSTALLED_APPS += [

]

MIDDLEWARE += [

]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8001",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8001",
]

DEBUG = True
