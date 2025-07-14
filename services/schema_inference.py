import pandas as pd


def infer_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "date"
    elif series.nunique() < 20:
        return "categorical"
    else:
        return "text"


def infer_schema(df):
    schema = []
    for col in df.columns:
        s = df[col]
        col_schema = {
            "column": col,
            "type": infer_type(s),
            "null_pct": s.isna().mean(),
            "n_unique": s.nunique()
        }
        schema.append(col_schema)
    return schema
