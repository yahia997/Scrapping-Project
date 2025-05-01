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

data1 = collection.aggregate([{
  '$project': {
    'comments.description': 1, 
    '_id': 0,
  },
}])

text = ''
for obj in data1:
  for desc in obj['comments']:
    text += desc['description']


col1, col2=st.columns([3,1])

stops = set(stopwords.words('english'))

cloud = WordCloud(width=1000, height=1000, stopwords=stops, background_color='white', colormap='magma').generate(text)
with col1:
    plt.figure(figsize=(8, 6))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()   
    st.pyplot(plt.gcf())

with col2:
   st.markdown("""
**The wordcloud is used to get insight into the most popular concepts or to reveal sentiment.**
    
-The wordcloud displayed here is used to get insights into the most popular words in the hotels' comment section.
            
-here we can see that staff is the most popular word, due to its size , also words like room, hotel, good, clean appeared alot.  """)