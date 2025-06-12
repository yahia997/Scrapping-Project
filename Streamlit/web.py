# This file combines pages and make the left navbar
import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", menu_items={ 'Get Help': None,'Report a bug': None,'About': None})
Main_page=st.Page('main_page.py',title='Main page', icon='🏨')
page_1 = st.Page("page_1.py", title="Comments wordcloud", icon="🏨")
page_2 = st.Page("page_2.py", title="Number of hotels in each city", icon="🏨")
page_3 = st.Page("page_3.py", title="Facility Count", icon="🏨")
page_5 = st.Page('page_5.py', title='Top 10 countries by num of hotels', icon='🏨')
page_7 = st.Page('page_7.py', title='Geographic Heatmap', icon='🏨')

pg = st.navigation([Main_page,page_1, page_2, page_3, page_5, page_7])

pg.run()

# In terminal to run the app type:
# streamlit run web.py