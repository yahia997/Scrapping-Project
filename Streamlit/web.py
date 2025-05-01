import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="expanded", menu_items={ 'Get Help': None,'Report a bug': None,'About': None})
Main_page=st.Page('main_page.py',title='Main page', icon='🏨')
page_1 = st.Page("page_1.py", title="1.Comments wordcloud", icon="🏨")
page_2 = st.Page("page_2.py", title="2.Number of hotels in each city", icon="🏨")
page_3 = st.Page("page_3.py", title="3.Facility Count", icon="🏨")
page_4 = st.Page('page_4.py', title='4.Facility average rating', icon='🏨')
page_5 = st.Page('page_5.py', title='5.Top 10 countries by num of hotels', icon='🏨')
page_6 = st.Page('page_6.py', title='6.Hotel price vs Rating', icon='🏨')

pg = st.navigation([Main_page,page_1, page_2, page_3, page_4, page_5, page_6])



pg.run()