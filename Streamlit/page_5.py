import matplotlib.pyplot as plt
import streamlit as st
from main_page import collection


data6 = collection.aggregate([
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
]).to_list()

topcountry = sorted(data6, key=lambda x: x["count"],reverse=True)[:10]

country = [entry['_id'] for entry in topcountry]
count = [entry['count'] for entry in topcountry]

col1, col2 =st.columns([2,1])
plt.figure(figsize=(8, 6))
plt.bar(country, count, color='mediumseagreen')
plt.title('Top 10 Countries commented on egyptian hotels')
plt.xlabel('Country')
plt.ylabel('Number of comments')
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()

with col1:
  st.pyplot(plt.gcf())