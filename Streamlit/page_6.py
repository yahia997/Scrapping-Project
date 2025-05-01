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


data7 = list(collection.aggregate([
  {
    '$match': {
      'price': {
        '$ne': None
      },
      'rating': {
        '$ne': None
      },
    }
  },
  {
    '$project': {
      '_id': 0,
      'rating': 1,
      'price': 1
    }
  }
]))

prices = [entry['price'] for entry in data7]
ratings = [entry['rating'] for entry in data7]

col1,col2=st.columns([2,1])

plt.figure(figsize=(8, 6))
plt.scatter(prices, ratings, color='red', edgecolor='black', s=77, alpha=0.7)
plt.xlabel('Price')
plt.ylabel('Rating')
plt.title('Hotel Price vs. Rating')
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.show()

with col1:
    st.pyplot(plt.gcf())

with col2:
    st.markdown('''
**Insights derived from the scatter plot**

-Most hotels fall in the 200:4000 price range, then they get less and less.

-There isn't a visible correlation between the hotel price and the rating.

-There is only a single hotel that costs more than 8000.


''')    