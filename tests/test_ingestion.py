from services.ingestion import load_file
from services.schema_inference import infer_schema
from services.schema_validation import validate_schema


def test_load_xlsx_file():
    df = load_file("tests/assets/file_example_XLSX_100.xlsx")
    assert df.shape[0] > 0


def test_schema_inference_returns_expected_keys():
    import pandas as pd
    df = pd.DataFrame({
        "name": ["A", "B", "C"],
        "amount": [10.0, 20.0, 30.0],
        "date": ["2023-01-01", "2023-01-02", "2023-01-03"]
    })
    schema = infer_schema(df)
    assert all(k in schema[0] for k in ["column", "type", "null_pct", "n_unique"])


def test_schema_validation_flags_nulls():
    schema = [
        {"column": "amount", "type": "numeric", "null_pct": 0.25, "n_unique": 10}
    ]
    alerts = validate_schema(schema)
    assert "amount" in alerts[0]

