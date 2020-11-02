from flask import Flask
from flask_caching import Cache

app = Flask(__name__)

cache = Cache(config={
    "CACHE_TYPE": "simple", 
    "CACHE_DEFAULT_TIMEOUT": 300
    })
cache.init_app(app)


from app import endpoints