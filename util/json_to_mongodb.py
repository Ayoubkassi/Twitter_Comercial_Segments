import json
from pymongo import MongoClient

# Connect to the MongoDB database
client = MongoClient('mongodb://localhost:27017/')
db = client['twitterScrap']


with open('../data/i_want_an_iphone_after_+10500_users_with_gender.json') as f:
    data = json.load(f)


collection = db['iphone_users']
result = collection.insert_many(data)

# # Read the JSON file
# with open('../data/i_want_an_iphone_after_+10500_users_with_gender.json') as f:
#     decoder = json.JSONDecoder()
#     data = f.read()
#     while data:
#         obj, idx = decoder.raw_decode(data)
#         data = data[idx:].lstrip()
#         collection.insert_one(obj)

# # Close the MongoDB connection
# client.close()
