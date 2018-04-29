""" Script to start the caching server """
from cache_server import app
from config import CONFIG

app.run(host=CONFIG["host"], port=CONFIG["port"], threaded=True)
