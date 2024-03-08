from lib.user_repository import UserRepository
from lib.user import User

""" 
When I call all on the user repository
I get all the users back in a list
"""

def test_list_all_users(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.all()
    assert result == [
        User(1, 'blob@hotmail.com'),
        User(2, 'email2@hotmail.com'),
        User(3, 'email3@email.com'),
        User(4, 'email4@email.com')
    ]

""" 
When I create a new user, it is successfully added to the user table
""" 

def test_create_new_user(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)

    repository.create_new_user(User(None, 'email5@email.com'))

    result = repository.all()
    assert result == [
        User(1, 'blob@hotmail.com'),
        User(2, 'email2@hotmail.com'),
        User(3, 'email3@email.com'),
        User(4, 'email4@email.com'),
        User(5, 'email5@email.com')
    ]

""" 
When I search for a single user, their email can be located and returned.
""" 
    
def test_find_user(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    user = repository.find_user('email3@email.com')
    assert user == User(3, 'email3@email.com')

""" 
When I search for a single user who isn't in the database, it is returned as an error
""" 
def test_find_non_user(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    attempt = repository.find_user('email7@email.com')
    assert attempt == None

"""
When an email is provided, if it is in the database, a log in message is returned
""" 

def test_check_email_exists(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.check_email_exists('email3@email.com')
    assert result == True

""" 
When an email is provided, if it is not in the database,
a message is returned asking the user to create an account.
""" 
def test_check_email_does_not_exist(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.check_email_exists('email7@email.com')
    assert result == False