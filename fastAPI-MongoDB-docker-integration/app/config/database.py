from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")

client = MongoClient(config.get("DATABASE_CONNECTION_URL"))

db = client.todo_app

collection_name = db["todos_app"]
