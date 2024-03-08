from lib.property_repository import *
from lib.property import *

'''
When we call PropertyRepository #all
We get a list of Property objects reflecting the seed data.

'''

def test_get_all_properties(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = PropertyRepository(db_connection)
    properties = repository.all()
    assert properties == [
        Property(1, 'Property1', 1, 'hot', 25.40 ),
        Property(2, 'Property2', 2, 'cold', 45.70),
        Property(3, 'Property3', 3, 'windy', 83),
        Property(4, 'Property4', 4, 'snow', 56.80),
        Property(5, 'Property5', 4, 'cloud', 83.20),
        ]
    
'''
When we add a property, it is added to the list of properties

'''

def test_add_property(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = PropertyRepository(db_connection)
    property_new = Property(None, 'Property6', 3, 'hello', 18.90)
    repository.add(property_new)
    properties = repository.all()
    assert properties == [
        Property(1, 'Property1', 1, 'hot', 25.40 ),
        Property(2, 'Property2', 2, 'cold', 45.70),
        Property(3, 'Property3', 3, 'windy', 83),
        Property(4, 'Property4', 4, 'snow', 56.80),
        Property(5, 'Property5', 4, 'cloud', 83.20),
        Property(6, 'Property6', 3, 'hello', 18.90)
        ]

'''
When we find a property, it is found based on the user 

'''

def test_find_property_by_user(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = PropertyRepository(db_connection)
    property_new = Property(None, 'Property6', 3, 'hello', 18.90)
    repository.add(property_new)
    test_user = 4
    filtered_list = repository.find_property_by_user_id(test_user)
    assert filtered_list == [
        Property(4, 'Property4', test_user, 'snow', 56.80),
        Property(5, 'Property5', test_user, 'cloud', 83.20),
        ]
    

'''
When there are no properties because the user has no properties, an empty list is outputted

'''

def test_find_property_no_properties_no_user(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = PropertyRepository(db_connection)
    property_new = Property(None, 'Property6', 3, 'hello', 18.90)
    repository.add(property_new)
    test_user = 6
    filtered_list = repository.find_property_by_user_id(test_user)
    assert filtered_list == []

'''
When we find a property, it is found based on the id of the property

'''

def test_find_property_by_property_id(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = PropertyRepository(db_connection)
    test_id = 2
    property = repository.find_property_by_id(test_id)
    assert property == Property(2, 'Property2', 2, 'cold', 45.70)
        


'''
No property is displayed if the id doesnt exist

'''

def test_find_property_by_property_id_no_id(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = PropertyRepository(db_connection)
    test_id = 9
    property = repository.find_property_by_id(test_id)
    assert property == "property not found"