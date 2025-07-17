import pandas as pd


def load_dataframe(uploaded_file):
    file_name = uploaded_file.name
    if file_name.endswith("csv"):
        return pd.read_csv(uploaded_file)
    elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format")
