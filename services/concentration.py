import pandas as pd
import numpy as np


def suggest_column_types(df, cat_unique_threshold=25):
    """
    Suggest likely columns for time, categorical, and numeric analysis based on heuristics.
    Returns a dict: {'time': [...], 'categorical': [...], 'numeric': [...]}
    """
    time_cols = [
        col for col in df.columns
        if "date" in str(col).lower()
        or "year" in str(col).lower()
        or "month" in str(col).lower()
        or pd.api.types.is_datetime64_any_dtype(df[col])
    ]
    categorical_cols = [
        col for col in df.columns
        if
        (
            df[col].dtype == 'object'
            or df[col].nunique() < cat_unique_threshold
        )
        and col not in time_cols
    ]
    numeric_cols = [
        col for col in df.columns
        if pd.api.types.is_numeric_dtype(df[col])
        and col not in time_cols
    ]
    return {
        "time": time_cols,
        "categorical": categorical_cols,
        "numeric": numeric_cols,
    }


def prepare_pivot(df, time_col, cat_col, num_col):
    """
    Group by category and period, sort, and pivot for cumulative analysis.
    """
    agg = df.groupby([cat_col, time_col])[num_col].sum().reset_index()
    agg_sorted = agg.sort_values(by=[time_col, num_col])
    agg_sorted['idx'] = agg_sorted.groupby(time_col).cumcount()
    df_pivot = agg_sorted.pivot(index='idx', columns=time_col, values=num_col).fillna(0)
    return df_pivot.astype(float)


def compute_bucket_matrix(cumsum, buckets):
    """
    For each bucket and period, find the minimal accumulated value reaching the given threshold.
    Returns:
        top: Matrix with the total value to reach the bucket in each period.
        n_rows: Matrix with the number of categories (rows) needed per bucket per period.
    """
    # 'total' is the sum of all values per period (last row of cumsum)
    total = cumsum.iloc[-1]
    n_buckets = len(buckets)
    n_periods = len(cumsum.columns)

    # 'acumulado_top' is the value that remains after removing the bucket percentage (e.g., 10%, 20%...)
    acumulado_top = np.array([total * (1 - q) for q in buckets])

    # 'acumulado_faltante' is how much needs to be accumulated for each bucket in each period
    acumulado_faltante = total.values.reshape(1, -1) - acumulado_top

    # Initialize the output matrices:
    # 'top' will store the minimum value required for each bucket and period
    # It starts with the total for each bucket (will be updated as we iterate)
    top = np.array([cumsum.copy().iloc[-1]] * n_buckets)
    # 'index_top' will store the number of rows needed to reach each bucket threshold
    index_top = np.zeros((n_buckets, n_periods))
    # 'zero_counts' counts when delta_matrix == 0 (special edge case)
    zero_counts = np.zeros((n_buckets, n_periods), dtype=int)

    i = 0
    # 'old_mask' tracks which entries have already reached their bucket threshold
    old_mask = zero_counts.copy().astype(bool)
    for _, row in cumsum.iloc[::-1].iterrows():
        i += 1
        # 'delta_matrix' is the difference between the total and the current accumulated value
        delta_matrix = np.array([total.values - row.values] * n_buckets)

        # For buckets already reached in previous iterations, keep the previous value
        mask = old_mask
        top[mask] = delta_matrix[mask]

        # Update the mask for buckets not yet reached (where we still need to accumulate)
        mask = (acumulado_faltante > delta_matrix).astype(bool)

        # 'index_matrix' represents how many rows we've processed so far (for each bucket and period)
        index_matrix = np.full((n_buckets, n_periods), i)
        # Store the row count when the bucket threshold is first reached
        index_top[mask] = index_matrix[mask]

        # 'mask_zero' identifies where the difference is exactly zero (special handling)
        mask_zero = delta_matrix == 0
        zero_counts += mask_zero.astype(int)

        # Update old_mask for next iteration (which buckets have been reached)
        old_mask = mask

    # Calculate the number of categories (rows) needed for each bucket/period
    n_rows = (index_top - zero_counts + 1).astype(int)
    return top, n_rows


def concentration_pivot(df, time_col, cat_col, num_col, buckets=[0.10, 0.20, 0.50], bucket_labels=None):
    """
    Returns two DataFrames:
    - df_top: total value required to reach each bucket for each period (buckets x periods)
    - df_n:   number of categories (rows) used to reach each bucket per period (buckets x periods)
    """
    if bucket_labels is None:
        bucket_labels = [f"Top {int(q*100)}%" for q in buckets]
    df_pivot = prepare_pivot(df, time_col, cat_col, num_col)
    cumsum = df_pivot.cumsum()
    top, n_rows = compute_bucket_matrix(cumsum, buckets)
    df_top = pd.DataFrame(top, index=bucket_labels, columns=df_pivot.columns)
    df_n = pd.DataFrame(n_rows, index=bucket_labels, columns=df_pivot.columns)
    return df_top, df_n
