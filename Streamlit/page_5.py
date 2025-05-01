from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json
from bson.objectid import ObjectId
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import nltk
from nltk.corpus import stopwords
import streamlit as st


load_dotenv()

uri = os.getenv('MONGODB_CONNECTION_STRING')
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Hotel'] # access database
collection = db['Hotel'] # access collection in a database


data6 = list(collection.aggregate([
  {'$unwind': '$comments'},
  {
    '$group': {
      '_id': '$comments.country',
      'count': {
        '$sum': 1
      }
    }
  },
  {
    '$match': {
      '_id': {
        '$regex': r'\w{2,}'
      }
    }
  },
  {
    '$sort': {
      'count': 1
    }
  }
]))

topcountry = sorted(data6, key=lambda x: x["count"],reverse=True)[:10]

country = [entry['_id'] for entry in topcountry]
count = [entry['count'] for entry in topcountry]

col1, col2 =st.columns([2,1])
plt.figure(figsize=(8, 6))
plt.bar(country, count, color='mediumseagreen')
plt.title('Top 10 Countries by Number of Hotels')
plt.xlabel('Country')
plt.ylabel('Number of Hotels')
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()

with col1:
    st.pyplot(plt.gcf())

with col2:

    st.markdown('''
**Insights derived from the bar chart**

**Egypt has the most number of hotels.**                

**Countries with the most hotels excluding Egypt:**
                                        
-United States   

-United Kingdom

-Saudi Arabia                                     

**Countries with the least hotels excluding Egypt:**
                                        
-Italy

-Turkey

-China                                                                                                                            
''')           