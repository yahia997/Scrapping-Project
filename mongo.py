# This file for just initializing and loading the database only

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

# to get environment vars
load_dotenv()

# connect to the database
uri = os.getenv('MONGODB_CONNECTION_STRING')
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
  print("You successfully connected to MongoDB!")
except Exception as e:
  print(e)

db = client['Hotel'] # access database
collection = db['Hotel'] # access collection in a database

######################################### for first time only #######################
# read cleaned json file
with open('cleaned_hotels.json', 'r',encoding='utf-8') as file:
  data = json.load(file)

# save to mongodb atlas
collection.insert_many(data)

# add revision for schema versioning
revision = 1
collection.update_many({}, {
  '$set': {
    'revision': revision
  }
})
######################################### ########################## #######################


# to close this connection as Free clusters are limited
client.close()