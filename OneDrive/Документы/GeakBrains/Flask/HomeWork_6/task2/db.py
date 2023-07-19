from pymongo import mongo_client
from settings import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)

db = client[settings.MONGO_INITDB_DATABASE]
tasks = db.tasks