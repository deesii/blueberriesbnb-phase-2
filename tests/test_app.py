from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection

# Tests for your routes go here

"""
We can render the index page
"""
def test_get_index(page, test_web_address, db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    page.goto(f"http://{test_web_address}/")

    h2_tag = page.locator("h2")
    # inputs = page.locator("input")
    # labels = page.locator("label")
    # button = page.get_by_role("button")

    expect(h2_tag).to_have_text("Property Listings")
    # expect(inputs).to_have_count(3)
    # expect(labels).to_have_count(2)
    # expect(button).to_have_count(1)
    

# def test_no_properties(page, test_web_address):
#     page.goto(f"http://{test_web_address}/index")
#     heading_tag = page.locator("h2")
#     expect(heading_tag).to_have_text("There are currently no properties to book.")

#     # # We load a virtual browser and navigate to the /index page
#     # #page.goto(f"http://{test_web_address}/index")

#     # We assert that it has the text "This is the homepage."
#     expect(strong_tag).to_have_text("This is the blueberries b&b homepage.")


'''
We can render the register page

'''
def test_render_register(page, test_web_address):
    page.goto(f"http://{test_web_address}/register")
    heading_tag = page.locator("h1")
    title_tag = page.locator("title")
    expect(heading_tag).to_have_text("Register")
    title_text = title_tag.inner_text()
    print("Actual title text:", title_text)
    #expect(title_tag).to_have_text("BlueberryBnB: Register") for some reason this appears to fail the test whereas the below text works.
    assert title_text == "BlueberryBnB: Register"


'''
We can render the add property page

'''

def test_render_property(page, test_web_address):
    page.goto(f"http://{test_web_address}/add_property")
    





"""
Test property information and booking page loads and has input fields with labels
"""

def test_get__individual_property(page, test_web_address, db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    page.goto(f"http://{test_web_address}/properties/1")

    h1_tag = page.locator("h1")
    inputs = page.locator("input")
    labels = page.locator("label")
    button = page.get_by_role("button")

    expect(h1_tag).to_have_text("Property1")
    expect(inputs).to_have_count(3)
    expect(labels).to_have_count(2)
    expect(button).to_have_count(1)

    page.goto(f"http://{test_web_address}/properties/2")
    
    h1_tag = page.locator("h1")
    inputs = page.locator("input")
    labels = page.locator("label")
    button = page.get_by_role("button")
    
    expect(h1_tag).to_have_text("Property2")
    expect(inputs).to_have_count(3)
    expect(labels).to_have_count(2)
    expect(button).to_have_count(1)


'''
When I call get/properties I see a list of the properties from the database

'''

# def test_get_all_properties(db_connection, web_client):
#     db_connection.seed("seeds/blueberries_bnb.sql")
#     response = web_client.get("/")
#     assert response.status_code == 200
#     assert response.data.decode("utf-8") == "" \
#         "Property(1, Property1, 1, hot, 25.40)\n"\
#         "Property(2, Property2, 2, cold, 45.70)\n"\
#         "Property(3, Property3, 3, windy, 83.00)\n"\
#         "Property(4, Property4, 4, snow, 56.80)\n"\
#         "Property(5, Property5, 4, cloud, 83.20)"
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
    get_response = web_client.get('/') 
    assert post_response.status_code == 200
    assert post_response.data.decode("utf-8") == ""
    assert get_response.status_code == 200
    # assert get_response.data.decode("utf-8") == "" \
    # "Property(1, Property1, 1, hot, 25.40)\n"\
    # "Property(2, Property2, 2, cold, 45.70)\n"\
    # "Property(3, Property3, 3, windy, 83.00)\n"\
    # "Property(4, Property4, 4, snow, 56.80)\n"\
    # "Property(5, Property5, 4, cloud, 83.20)\n"\
    # "Property(6, Property6, 3, wet, 23.40)"



'''
When one of the inputs are not included, when I post a new property via POST/add_property I will see an error message, when trying to add to database

'''

def test_post_property_incomplete(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    response = web_client.post('/add_property', data = {'user_id': "3", 'description' : "wet", 'price_per_night' : "23.40"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == 'One of the inputs is not filled in!'
