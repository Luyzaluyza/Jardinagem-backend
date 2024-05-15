from flask import Flask
from pymongo import MongoClient
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGO_URI'])
db = client['User']
