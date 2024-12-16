from pymongo import MongoClient  
from config import DATABASE_URL

mongo_client = MongoClient(DATABASE_URL)
db = mongo_client['hehe']  
users = db['users']
