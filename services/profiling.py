from ydata_profiling import ProfileReport
import tempfile


def generate_profile_html(df):
    profile = ProfileReport(df, minimal=True)
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        profile.to_file(tmp.name)
        return open(tmp.name, encoding="utf-8").read()
