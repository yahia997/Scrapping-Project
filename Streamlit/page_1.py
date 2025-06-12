import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import streamlit as st

from main_page import collection

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