import pandas as pd
from services.profiling import generate_profile_html


def test_generate_profile_html_basic():
    df = pd.DataFrame({
        "Feature A": [1, 2, 3],
        "Feature B": ["x", "y", "z"],
        "Feature C": [1.1, 2.2, 3.3]
    })

    html = generate_profile_html(df)
    print(html[:500])
    assert "<body" in html
