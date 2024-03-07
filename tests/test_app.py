from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We look at the <p> tag
    strong_tag = page.locator("p")

    # We assert that it has the text "This is the homepage."
    expect(strong_tag).to_have_text("This is the blueberries b&b homepage.")


'''
When I call get/properties I see a list of the properties from the database

'''

def test_get_properties(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql")
    response = web_client.get("/properties")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "" \
        "Property(1, Property1, 1, hot, 25.40)\n"\
        "Property(2, Property2, 2, cold, 45.70)\n"\
        "Property(3, Property3, 3, windy, 83.00)\n"\
        "Property(4, Property4, 4, snow, 56.80)\n"\
        "Property(5, Property5, 4, cloud, 83.20)"
## create route
## return 200
## return a list of properties from the database
    # "Property(1, Property1, 1, hot, 25.40)\n"\
    #  "Property(2, Property2, 2, cold, 45.70)\n"\
    #     "Property(3, Property3, 3, windy, 83)\n"\
    #     "Property(4, Property4, 4, snow, 56.80)\n"\
    #     "Property(5, Property5, 5, cloud, 83.20)"

'''
When I post a new property via POST/index I see a list of the properties with the additional property from the database

'''
def test_post_property(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    post_response = web_client.post('/add_property', data = {'property_name': "Property6", 'user_id': "3", 'description' : "wet", 'price_per_night' : "23.40"})
    get_response = web_client.get('/properties') 
    assert post_response.status_code == 200
    assert post_response.data.decode("utf-8") == ""
    assert get_response.status_code == 200
    assert get_response.data.decode("utf-8") == "" \
    "Property(1, Property1, 1, hot, 25.40)\n"\
    "Property(2, Property2, 2, cold, 45.70)\n"\
    "Property(3, Property3, 3, windy, 83.00)\n"\
    "Property(4, Property4, 4, snow, 56.80)\n"\
    "Property(5, Property5, 4, cloud, 83.20)\n"\
    "Property(6, Property6, 3, wet, 23.40)"



'''
When one of the inputs are not included, when I post a new property via POST/add_property I will see an error message, when trying to add to database

'''

def test_post_property_incomplete(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    response = web_client.post('/add_property', data = {'user_id': "3", 'description' : "wet", 'price_per_night' : "23.40"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == 'One of the inputs is not filled in!'

