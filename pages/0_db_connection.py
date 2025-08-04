import streamlit as st
from pathlib import Path
import os
from dotenv import load_dotenv
import check_db

# Load environment variables
load_dotenv()

st.set_page_config(page_title="GraphiteVision Analytics - DB Connection", layout="wide")

# Logo in upper right
logo_path = Path("resources/static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Database Connection Status")
st.markdown("""
This page displays the current status of the database connection and relevant details.
""")

st.subheader("Connection Details")

try:
    db_status, db_info = check_db.check_database_connection()
    
    if db_status:
        st.success("Database Connection: Connected")
        st.write(f"**Database Name:** {db_info.get('database_name', 'N/A')}")
        st.write(f"**Database Type:** {db_info.get('database_type', 'N/A')}")
        st.write(f"**Connection String/Path:** {db_info.get('connection_string', 'N/A')}")
        st.write(f"**Tables Found:** {db_info.get('tables_found', 'N/A')}")
        st.write(f"**Columns Found:** {db_info.get('columns_found', 'N/A')}")
        
        if 'error_message' in db_info and db_info['error_message']:
            st.warning(f"Additional Info/Warnings: {db_info['error_message']}")
            
    else:
        st.error("Database Connection: Disconnected or Failed")
        if 'error_message' in db_info:
            st.exception(db_info['error_message'])
        else:
            st.write("Could not establish a connection to the database.")

except Exception as e:
    st.error("An error occurred while trying to check the database connection.")
    st.exception(e)