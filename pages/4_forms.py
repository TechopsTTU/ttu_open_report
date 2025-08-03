import streamlit as st
from pathlib import Path

# Logo in upper right
logo_path = Path("static/TTU_LOGO.jpg")
if logo_path.exists():
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image(str(logo_path), width=120)

st.title("Data Entry Portal")
st.markdown("""
Enter new data and submit forms through this secure portal. Try out the sample form below to test functionality.
""")

with st.form("entry_form"):
    st.write("Sample Data Entry Form")
    field1 = st.text_input("Field 1", "Sample Value")
    field2 = st.number_input("Field 2", min_value=0, value=10)
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success(f"Form submitted! Field 1: {field1}, Field 2: {field2}")
