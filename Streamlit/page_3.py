import matplotlib.pyplot as plt
import streamlit as st
from main_page import collection
import numpy as np

data3 = collection.aggregate([
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
]).to_list()

tops = sorted(data3, key=lambda x: x['count'], reverse=True)[:10]

facilities = [doc["_id"] for doc in tops]
counts = [doc["count"] for doc in tops]
rating = [doc["avg_rating"] for doc in tops]

x = np.arange(len(facilities))
width = 0.35 

col1, col2=st.columns([3,1])

with col1:
  fig, ax = plt.subplots(figsize=(8, 6))
  bars1 = ax.bar(x - width/2, counts, width, label='Count', color='skyblue')
  bars2 = ax.bar(x + width/2, rating, width, label='Avg Rating', color='salmon')
  # Labels and formatting
  ax.set_ylabel('Value')
  ax.set_title('Facility Count and Average Rating')
  ax.set_xticks(x)
  ax.set_xticklabels(facilities, rotation=25, ha='right')
  ax.legend()
  ax.grid(True, linestyle='--', alpha=0.5)
  plt.tight_layout()
  plt.show()
  st.pyplot(plt.gcf())
