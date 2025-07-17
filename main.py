import streamlit as st
import pandas as pd
from services.ingestion import load_dataframe
from services.profiling import generate_profile_html
from services.concentration import concentration_pivot, suggest_column_types

st.set_page_config(page_title="Investment Analyzer", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Upload"

pages = ["Upload", "Data Overview", "Analyze"]
selected = st.sidebar.radio("Navigation", pages)

if selected == "Upload":
    st.session_state.page = "Upload"
    st.title("Upload your Excel")
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "csv"])
    if uploaded_file:
        df = load_dataframe(uploaded_file)
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['df'] = df
        st.success("File uploaded!")

elif selected == "Data Overview":
    st.title("Data Overview")
    df = st.session_state.get('df', None)
    if df is not None:
        st.subheader("Preview of your data")
        st.dataframe(df.head(30))

        st.subheader("Profiling Report")
        with st.spinner("Generating profile report..."):
            html = generate_profile_html(df)
            st.components.v1.html(html, height=1000, scrolling=True)
    else:
        st.info("No data to display. Please upload a file first.")
        
elif selected == "Analyze":
    st.title("Analyze: Concentration Analysis")
    df = st.session_state.get('df', None)

    if df is not None:
        # Detect columns dinamicamente
        col_types = suggest_column_types(df)

        st.write("Choose columns for your analysis:")

        time_col = st.selectbox("Time column (period)", col_types['time'])
        cat_col = st.selectbox("Category column (for grouping)", col_types['categorical'])
        num_col = st.selectbox("Numeric column (to aggregate)", col_types['numeric'])

        if st.button("Run Concentration Analysis"):
            st.info("Calculating...")

            # Gera a tabela pivot usando a nova função robusta
            pivot_df, _ = concentration_pivot(df, time_col, cat_col, num_col)

            st.subheader("Concentration Table (buckets x period)")
            st.dataframe(pivot_df.style.format("{:,.2f}"))

            # Gráfico dos Top 10/20/50% ao longo do tempo
            st.subheader("Top 10/20/50% Over Time")
            chart_data = pivot_df.loc[["Top 10%", "Top 20%", "Top 50%"]].T
            st.line_chart(chart_data)

    else:
        st.info("No data available. Please upload a file first.")
