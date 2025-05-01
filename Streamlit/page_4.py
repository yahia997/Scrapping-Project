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

data3 = list(collection.aggregate([
  {'$unwind': '$facilities'}, # deconstruct array elements
  {
    '$group': {
      '_id': '$facilities',
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
      }
    }
  }
]))

tops = sorted(data3, key=lambda x: x['count'], reverse=True)[:10]

facilities = [doc["_id"] for doc in tops]
counts = [doc["count"] for doc in tops]
rating = [doc["avg_rating"] for doc in tops]

x = np.arange(len(facilities))
width = 0.35

col1, col2=st.columns([7,3])

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
bars2 = ax.bar(x + width/2, rating, width, label='Avg Rating', color='salmon')
# Labels and formatting
ax.set_ylabel('Value')
ax.set_title('Facility Average Rating')
ax.set_xticks(x)
ax.set_xticklabels(facilities, rotation=25, ha='right')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

with col1:
    st.pyplot(plt.gcf())

with col2:
    st.markdown('''
**Insights derived from the bar chart**

**All the facilites have a decent avg rating, and they are all close to each other.**
                                
**Highest avg rating:**
                                        
-Airport shuttle   

-Room service

-Resturant                                     

**Lowest avg rating:**
                                        
-Free parking

-Family rooms

-Free wifi                                                                                                                            
''')            