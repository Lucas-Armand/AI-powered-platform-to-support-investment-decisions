import streamlit as st

st.set_page_config(page_title="Investment Analyzer", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Upload"

pages = ["Upload", "Normalize", "Analyze"]
selected = st.sidebar.radio("Navigation", pages)

if selected == "Upload":
    st.session_state.page = "Upload"
    st.title("Upload your Excel")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])
    if uploaded_file:
        st.session_state['uploaded_file'] = uploaded_file
        st.success("File uploaded!")
elif selected == "Normalize":
    st.title("Fix & Normalize Data")
    st.write("Coming soon…")
elif selected == "Analyze":
    st.title("Analyze & Get Insights")
    st.write("Coming soon…")
    
