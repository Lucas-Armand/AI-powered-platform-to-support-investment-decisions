from streamlit.testing.v1 import AppTest

def test_default_page_is_upload():
    at = AppTest.from_file("main.py")
    at.run()
    assert at.title[0].value.startswith("Upload")

def test_navigation_to_data_overview():
    at = AppTest.from_file("main.py")
    at.run()
    at.sidebar.radio[0].set_value("Data Overview")
    at.run()
    assert "Overview" in at.title[0].value

def test_navigation_to_analyze():
    at = AppTest.from_file("main.py")
    at.run()
    at.sidebar.radio[0].set_value("Analyze")
    at.run()
    assert "Concentration Analysis" in at.title[0].value

