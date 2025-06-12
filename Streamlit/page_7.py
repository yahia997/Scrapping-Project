import streamlit as st
from main_page import collection
import streamlit as st
import plotly.express as px
import pandas as pd

data2 = collection.aggregate([
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
}]).to_list()

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