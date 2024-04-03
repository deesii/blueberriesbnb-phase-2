import pytest, sys, random, py, pytest, os
from xprocess import ProcessStarter
from lib.database_connection import DatabaseConnection
from app import app
from playwright.sync_api import sync_playwright
from werkzeug.security import check_password_hash, generate_password_hash
from lib.user_repository import UserRepository

EMAIL_PASSWORD_MAP = {
    'blob@hotmail.com': 'testing0&',
    'email2@hotmail.com': 'testing1!',
    'email3@email.com': '&1testing',
    'email4@email.com': '8^testing',
}

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
        

# hashing the password before putting into the tests for our seeds
@pytest.fixture
def update_seed_file_with_hashes():
    def hash_password(password):
        return generate_password_hash(password)
    
    def create_update_seed_file(seed_file_path):
        with open(seed_file_path, 'r') as f:
            seed_content = f.read()

        updated_seed_content = seed_content

        for email, password in EMAIL_PASSWORD_MAP.items():
                hashed_password = hash_password(password)
                updated_seed_content = updated_seed_content.replace(f"INSERT INTO users (email, password) VALUES ('{email}', NULL);", f"INSERT INTO users (email, password) VALUES ('{email}', '{hashed_password}');")

        with open(seed_file_path, 'w') as f:
            f.write(updated_seed_content)
        

    return create_update_seed_file


