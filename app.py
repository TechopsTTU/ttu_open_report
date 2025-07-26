
import streamlit as st

st.set_page_config(page_title="TTU Open Report", layout="wide")
st.sidebar.title("Navigation")
st.sidebar.markdown(
    """
    - [Tables](tables)
    - [Queries](queries)
    - [Reports](reports)
    - [Forms](forms)
    """
)
# Removed st.write() to keep only sidebar navigation
