import matplotlib.pyplot as plt
import streamlit as st
from main_page import collection

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
  },
}]).to_list()

print(data2)

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
    