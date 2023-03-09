import json
from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterScrap']
collection = db['users']

# Read the JSON file
with open('../apple_users.json') as f:
    decoder = json.JSONDecoder()
    data = f.read()
    while data:
        obj, idx = decoder.raw_decode(data)
        data = data[idx:].lstrip()
        collection.insert_one(obj)

# Close the MongoDB connection
client.close()
