from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import pandas as pd

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



col1,col2=st.columns([2,1])

with col1:
    df = pd.DataFrame(data2)
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="_id",
        size="count",      
        color="avg_rating",
        color_continuous_scale="Viridis",
        zoom=5,
        height=600,
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)


with col2:
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('')
    st.markdown('''
                **Insights derived from the map**

                **Top cities by average rating:**

                -North Coast

                -Marsa Alam

                -Dahab

                **Bottom cities by average rating:**

                -Ismailia

                -Fayoum

                -Cairo
                ''')        