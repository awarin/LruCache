from flask import Flask

app = Flask(__name__)

from cache_server import routes
