from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

def load(data):
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

  revision = 1
  print("Loading to MongoDB ...")
  print(f"Schema version is {revision}")
  try: 
    db = client['Hotel'] # access database
    collection = db['Hotel'] # access collection in a database
    
    collection.create_index(['title'])

    # save to mongodb atlas
    collection.insert_many(data)

    # add revision for schema versioning
    collection.update_many({}, {
      '$set': {
        'revision': revision
      }
    })

    # to close this connection as Free clusters are limited
    client.close()
  except Exception :
    print("Loading failed to MongoDB !!!")

  print("Loaded Successfully to MongoDB")