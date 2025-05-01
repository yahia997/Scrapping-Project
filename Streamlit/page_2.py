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

uri = "mongodb+srv://read:GyXXtAnGawVA68YX@cluster0.nsusqff.mongodb.net/?appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client['Hotel'] # access database
collection = db['Hotel'] # access collection in a database

data2 = list(collection.aggregate([
  {
  '$match': {
    'city': {
        '$exists': True,
        '$ne': None
      }
    },
  },{
  '$group': {
    '_id': '$city', 
    'count': {
      '$sum': 1
    },
    'avg_rating': {
      '$avg': {
        '$ifNull': ['$rating', 0]
      }
    },
    'avg_price': {
      '$avg': {
        '$ifNull': ['$price', 0]
      }
    },
    'latitude': {
      '$avg': {
        '$ifNull': ['$latitude', 0]
      }
    },
    'longitude': {
      '$avg': {
        '$ifNull': ['$longitude', 0]
      }
    },
  },
}]))

cities = [doc['_id'] for doc in data2]
counts = [doc['count'] for doc in data2]

col1, col2=st.columns([3,1])

with col1:
    plt.figure(figsize=(7, 4))
    plt.bar(cities, counts, color='skyblue')
    plt.title('Number of Hotels in Each City')
    plt.xlabel('City')
    plt.ylabel('Hotel Count')
    plt.xticks(rotation=35)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    st.pyplot(plt.gcf(),use_container_width=True)

with col2:
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('''
**Insights derived from the bar chart**

-Hurghada has the most hotels
                
-North Coast has the least hotels
                
-Most cities has around 25 hotels
''')
    