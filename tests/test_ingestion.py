import os
import io
import pytest
from services.ingestion import load_dataframe

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

def make_uploaded_file(path):
    # Lê o conteúdo binário do arquivo
    with open(path, "rb") as f:
        content = f.read()
    uploaded = io.BytesIO(content)
    uploaded.name = os.path.basename(path)
    return uploaded

def test_load_csv_utf8():
    file_path = os.path.join(ASSETS_PATH, "sample_utf8.csv")
    uploaded = make_uploaded_file(file_path)
    df = load_dataframe(uploaded)
    assert not df.empty
    assert list(df.columns) == ["Field1", "Field2", "Field3"]

def test_load_xlsx_example():
    file_path = os.path.join(ASSETS_PATH, "file_example_XLSX_100.xlsx")
    uploaded = make_uploaded_file(file_path)
    df = load_dataframe(uploaded)
    assert "First Name" in df.columns
    assert len(df) >= 5
