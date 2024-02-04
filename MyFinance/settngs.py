#settings.py
from os import environ
from dotenv import load_dotenv

load_dotenv()

PGURI = environ.get('PGURI')