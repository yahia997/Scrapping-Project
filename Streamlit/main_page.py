import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import pandas as pd

# Connect to the the cluster
load_dotenv()

uri = os.getenv('MONGODB_CONNECTION_STRING')
client = MongoClient(uri, server_api=ServerApi('1'))

st.title('🏨 Hotel Analytics Dashboard')

# Send a ping to confirm a successful connection
try:
  print("You successfully connected to MongoDB!")
  db = client['Hotel'] # access database
  collection = db['Hotel'] # access collection in a database

  all = collection.aggregate([{
    '$project': {
        'title': 1,
        '_id': 1
    }
  }]).to_list()

  df = pd.DataFrame(all)
  
  hotel = st.selectbox('Hotel', df[['title']])
  id = df[df['title'] == hotel]['_id'].iloc[0]
  data = collection.find_one(id)

  st.markdown(f'''
  You have {len(all)} hotel in your database now
''')
  
  st.markdown(f'''
  ## {data['title']} 
  url: {data['url']}

  time of scrapping: {data['date']}

  #### Description:

  {data['description']}

  **Facilities**: {', '.join(data['facilities'])}
  ''')
except Exception as e:
  print(e)


