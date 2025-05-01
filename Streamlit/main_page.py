import streamlit as st

st.title('🏨 Hotel Analytics Dashboard')

st.subheader('Analysing global hotel data')
st.divider()

st.markdown("""
**This interactive dashboard helps you analyze hotel data worldwide.
Discover relationships between price and ratings, facility availability,
and geographic distributions.**
""")

with st.expander("📊 Main Features", expanded=True):
        st.success("• Common comments")
        st.success("• Price vs. Rating analysis")
        st.success("• Facility count and quality")
        st.success("• Geographic hotel distribution")


