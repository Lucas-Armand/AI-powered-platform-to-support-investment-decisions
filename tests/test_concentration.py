import pandas as pd
import numpy as np
from services.concentration import prepare_pivot, compute_bucket_matrix, concentration_pivot, suggest_column_types


def test_prepare_pivot_basic():
    df = pd.DataFrame({
        "period": [2020, 2020, 2021, 2021],
        "cat": ["A", "B", "A", "B"],
        "val": [10, 20, 30, 40]
    })

    pivot = prepare_pivot(df, "period", "cat", "val")

    assert isinstance(pivot, pd.DataFrame)
    assert set(pivot.columns) == {2020, 2021}
    assert np.allclose(pivot.sum().values, [30, 70])  # Totals per year


def test_compute_bucket_matrix_simple():
    cumsum = pd.DataFrame({
        2020: [10, 20, 30],
        2021: [20, 50, 70]
    })
    buckets = [0.10, 0.50]

    top, n_rows = compute_bucket_matrix(cumsum, buckets)

    assert top.shape == (2, 2)
    assert n_rows.shape == (2, 2)
    assert np.all(top >= 0)
    assert np.all(n_rows >= 1)


def test_suggest_column_types_detects_types():
    df = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "month": [1, 2, 3],
        "date": pd.to_datetime(["2020-01-01", "2021-02-01", "2022-03-01"]),
        "region": ["East", "West", "East"],
        "revenue": [100, 200, 300]
    })

    result = suggest_column_types(df)

    assert "date" in result["time"] or "year" in result["time"]
    assert "region" in result["categorical"]
    assert "revenue" in result["numeric"]


def test_concentration_pivot_edge_empty_bucket():
    df = pd.DataFrame({
        'year': [2020]*3,
        'value': [100, 0, 0],
        'name': ['a', 'b', 'c']
    })

    df_top, df_n = concentration_pivot(df, "year", "name", "value")

    assert df_top.loc["Top 10%", 2020] == 100
    assert df_n.loc["Top 10%", 2020] == 1


def test_concentration_pivot_all_buckets_same_if_one_client():
    df = pd.DataFrame({
        'year': [2020, 2021, 2022],
        'value': [50, 100, 200],
        'name': ['the_only', 'the_only', 'the_only']
    })
    df_top, df_n = concentration_pivot(df, "year", "name", "value")
    for bucket in df_top.index:
        assert (df_top.loc[bucket] == [50, 100, 200]).all()
        assert (df_n.loc[bucket] == 1).all()
