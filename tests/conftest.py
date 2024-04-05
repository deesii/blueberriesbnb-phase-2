import pytest, sys, random, py, pytest, os
from xprocess import ProcessStarter
from lib.database_connection import DatabaseConnection
from app import app
from playwright.sync_api import sync_playwright, Page, expect



# This is a Pytest fixture.
# It creates an object that we can use in our tests.
# We will use it to create a database connection.
@pytest.fixture
def db_connection():
    conn = DatabaseConnection(test_mode=True)
    conn.connect()
    return conn

# This fixture starts the test server and makes it available to the tests.
# You don't need to understand it in detail.
@pytest.fixture
def test_web_address(xprocess):
    python_executable = sys.executable
    app_file = py.path.local(__file__).dirpath("../app.py")
    port = str(random.randint(4000, 4999))
    class Starter(ProcessStarter):
        env = {"PORT": port, "APP_ENV": "test", **os.environ}
        pattern = "Debugger PIN"
        args = [python_executable, app_file]

    xprocess.ensure("flask_test_server", Starter)

    yield f"localhost:{port}"

    xprocess.getinfo("flask_test_server").terminate()


# Now, when we create a test, if we allow it to accept a parameter called
# `db_connection` or `test_web_address`, Pytest will automatically pass in the
# objects we created above.

# For example:

def test_something(db_connection, test_web_address):
    pass


# We'll also create a fixture for the client we'll use to make test requests.
@pytest.fixture
def web_client():
    app.config['TESTING'] = True # This gets us better errors
    with app.test_client() as client:
        yield client

# @pytest.fixture(scope="module")
# def page():
#     with sync_playwright() as p:
#         browser = p.chromium.launch()
#         page = browser.new_page()
#         yield page
#         browser.close()
        
@pytest.fixture
def login(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    page.fill("input[name=email]", "blob@hotmail.com")
    page.screenshot(path="screenshot1.png", full_page=True)
    page.click("#submit_login")
    page.screenshot(path="screenshot.png", full_page=True)
    return 
