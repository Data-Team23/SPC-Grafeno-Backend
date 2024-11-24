from pymongo import MongoClient

client = MongoClient(
    'mongodb://mongo_user:mongo_password@mongodb:27017/'
)

logs_db = client['logs']
encrypt_db = client['encrypt']
