from playwright.sync_api import Page, expect
from lib.database_connection import DatabaseConnection

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
We can render the add property page, and has the input fields with labels

'''

def test_render_property(page, test_web_address):
    page.goto(f"http://{test_web_address}/add_property")
    heading_tag = page.locator("h1")
    title_tag = page.locator("title")
    expect(heading_tag).to_have_text("Add New Property")
    title_text = title_tag.inner_text()
    print(f"title text is : {title_text}")
    #expect(title_tag).to_have_text("BlueberryBnB: Add New Property") --> unsure why this doesnt behave accordingly
    assert title_text == "BlueberryBnB: Add New Property"
    labels = page.locator("label")
    text_inputs = page.locator("input[type='text']")
    submit_inputs = page.locator("input[type='submit']")
    textarea = page.locator("textarea")
    expect(labels).to_have_count(3)
    expect(text_inputs).to_have_count(2)
    expect(submit_inputs).to_have_count(1)
    expect(textarea).to_have_count(1)
    expect(submit_inputs).to_have_attribute("value","Add Property")

    input_items = page.locator("input[type='text']").all()
    print(input_items)

    id_names = ["property_name", "price_per_night"]

    for index, id_name in enumerate(id_names):
        input_element = input_items[index] 
        expect(input_element).to_have_attribute("id",id_name)

        print(f"the input element is {input_element} and the id should be {id_names[index]}")



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

# """
# Bookings are listed for current user
# """
# def test_bookings_list(page, test_web_address, db_connection):
#     db_connection.seed("seeds/blueberries_bnb.sql")
#     page.goto(f"http://{test_web_address}/bookings")
#     h1 = page.locator("h1")
#     h2 = page.locator("h2")
#     divs = page.locator("div")
    
#     expect(h1).to_have_text("Bookings")
#     # expect(h2).to_have_text(["Pending", "Approved"])
#     # expect(divs).to_have_text([
#     #     "Property Name: Property1\nBooked from 2024-03-27 till 2024-03-29",
#     #     "Property Name: Property3\nBooked from 2024-07-01 till 2024-07-10"
#     # ])

"""
Booking is added when it is submitted via booking form
"""
def test_add_booking(page, test_web_address, db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    page.goto(f"http://{test_web_address}/properties/1")
    page.screenshot(path="screenshot.png", full_page=True)
    page.fill("input[name=date_from]", "2024-03-13")
    page.screenshot(path="screenshot.png", full_page=True)
    page.fill("input[name=date_to]", "2024-03-15")
    page.screenshot(path="screenshot.png", full_page=True)
    page.click("text=Create Booking")





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

When I GET/my_properties I am redirected to the login.html page if  I am not logged in

'''
def test_not_logged_in_get_my_properties_redirect(db_connection, web_client, page, test_web_address):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    response = web_client.get("/my_properties")
    assert response.status_code == 302
    
    page.goto(f"http://{test_web_address}/my_properties")
    
    h1_tag = page.locator("h1")
    title_tag = page.locator("title")
    title_text = title_tag.inner_text()
    print("Actual title text:", title_text)
    expect(h1_tag).to_have_text("Login")
    assert title_text == "BlueberryBnB: Login"



# '''
# When I GET/my_properties I see a list of my properties if  I am logged in

# '''

# #flask app not handling session data, and appears to not recognise the session data!, or it is an issue with playwright handling?

# def test_get_my_properties(db_connection, web_client, page, test_web_address):
#     db_connection.seed("seeds/blueberries_bnb.sql") 

#     with web_client.session_transaction() as session:
#         session['user_id'] = '3'
    
#     print(f"before going to the page : {session['user_id']}")
    
#     page.goto(f"http://{test_web_address}/my_properties")
    
#     print(f"after going to the page: {session['user_id']}")
#     h1_tag = page.locator("h1")
#     print(f"h1 tag text is {h1_tag.inner_text()}")
#     title_tag = page.locator("title")
#     title_text = title_tag.inner_text()
#     print("Actual title text:", title_text)
#     expect(h1_tag).to_have_text("My properties")
#     assert title_text == "BlueberryBnB: My properties"
#     list_items = page.locator("#my-property-listings ul > li")
#     expect(list_items).to_contain_text([
#         "Property3 - Description: windy - Price per night 83.0",
#     ])


'''
When I post a new property via POST/add_property it redirects to the index page

'''
def test_post_property(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql") 

    with web_client.session_transaction() as session:
        session['user_id'] = '3'
    post_response = web_client.post('/add_property', data = {'property_name': "Property6", 'description' : "wet", 'price_per_night' : "23.40"})
    redirect_response = web_client.get('/') 
    assert post_response.status_code == 302
    assert redirect_response.status_code == 200

'''
When I post a new property via POST/add_property it redirects to the index page and I see the list of properties with the added property

'''
def test_post_property_get_index_page(db_connection, web_client, page, test_web_address):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    with web_client.session_transaction() as session:
        session['user_id'] = '3'
    post_response = web_client.post('/add_property', data = {'property_name': "Property6", 'description' : "wet", 'price_per_night' : "23.40"})
    redirect_response = web_client.get('/') 
    assert post_response.status_code == 302
    assert redirect_response.status_code == 200
    page.goto(f"http://{test_web_address}/")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("Property Listings")
    list_items = page.locator("#property-listings ul > li")
    expect(list_items).to_contain_text([
        "Property1 - Description: hot - Price per night 25.4",
        "Property2 - Description: cold - Price per night 45.7",
        "Property3 - Description: windy - Price per night 83.0",
        "Property4 - Description: snow - Price per night 56.8",
        "Property5 - Description: cloud - Price per night 83.2",
        "Property6 - Description: wet - Price per night 23.4"
    ])
    

'''
When one of the inputs are not included, when I post a new property via POST/add_property I will see an error message, when trying to add to database

'''

def test_post_property_incomplete(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    with web_client.session_transaction() as session:
        session['user_id'] = '3'
    response = web_client.post('/add_property', data = {'description' : "wet", 'price_per_night' : "23.40"})
    assert response.status_code == 400
    assert response.data.decode('utf-8') == 'One of the inputs is not filled in!'


'''
When you click on the logout page, you hve the status code for redirecting to the index page

'''

def test_logout_redirect(db_connection, web_client):
    db_connection.seed("seeds/blueberries_bnb.sql") 
    response = web_client.get('/logout')
    assert response.status_code == 302 


# '''
# When I click on the logout page, the session clear actually takes place
# '''

# def test_logout_clears_session(test_web_address, page, db_connection, web_client):
#     db_connection.seed("seeds/blueberries_bnb.sql") 
#     with web_client.session_transaction() as session:
#         session['user_id'] = '3'
#     page.goto(f"http://{test_web_address}/")
#     page.click('a.nav-link[href="/logout"]')
    
    
#     page.wait_for_navigation(timeout=60000)
    
#     #page.goto(f"http://{test_web_address}/logout")
    
#     with web_client.session_transaction() as session:
#         assert 'user_id' not in session