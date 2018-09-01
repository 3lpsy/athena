from os import environ
from flask import Flask

app = Flask(environ.get('WEB_APP_NAME', 'athena'))
