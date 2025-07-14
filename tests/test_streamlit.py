from streamlit.testing.v1 import AppTest

def test_default_page_is_upload():
    at = AppTest.from_file("app/streamlit_ui.py")
    at.run()
    assert at.title[0].value.startswith("Upload")

def test_navigation_to_normalize():
    at = AppTest.from_file("app/streamlit_ui.py")
    at.run()
    at.sidebar.radio[0].set_value("Normalize")
    at.run()
    assert at.title[0].value.startswith("Fix & Normalize")

def test_navigation_to_analyze():
    at = AppTest.from_file("app/streamlit_ui.py")
    at.run()
    at.sidebar.radio[0].set_value("Analyze")
    at.run()
    assert at.title[0].value.startswith("Analyze & Get")
    
