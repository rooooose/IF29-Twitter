import pymongo
from pymongo import MongoClient
from config import config 

client =  MongoClient('mongodb+srv://'+ config.MANGODB_USERNAME + ':' + config.MANGODB_PASSWORD + '@cluster0.rb8pj.mongodb.net/')
db = client['if29']
collection = db['set1']
    
def findOne(option = None):
    return collection.find_one(option)

def find(option = None):
    return collection.find(option)