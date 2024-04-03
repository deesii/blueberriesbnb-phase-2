from lib.user_repository import UserRepository
from lib.user import User
from werkzeug.security import check_password_hash,generate_password_hash



def test_correct_hashing_password(db_connection, update_seed_file_with_hashes):
    seed_file_path = 'seeds/blueberries_bnb.sql'
    update_seed_file_with_hashes(seed_file_path)
    db_connection.seed(seed_file_path)
    repository = UserRepository(db_connection)
    user = repository.find_user('blob@hotmail.com')
    assert check_password_hash(user.password, "testing0") == True
    assert check_password_hash(user.password, "tess23ing18") == False
    

""" 
When I call all on the user repository
I get all the users back in a list (prior to hashing password)
"""

def test_list_all_users(db_connection):
    seed_file_path = 'seeds/blueberries_bnb.sql'
    db_connection.seed(seed_file_path)
    repository = UserRepository(db_connection)
    result = repository.all()
    assert result == [
        User(1, 'blob@hotmail.com', 'scrypt:32768:8:1$M60JBIdOoYHi08nh$137a9beb34d68195ddf14648e2f56a4763e5514ddda166c8f24b8a19a439e8eea76693c056dfe379652210637a5cd31cd334e642773518dbb20cf4554cf80322'),
        User(2, 'email2@hotmail.com', 'scrypt:32768:8:1$VHIoPXPuUnh06Q0z$03481d7e4881aa6d4ec6536fb3b237eb31f5d6a295c40ec91018232c08e63e1d7134711f07012f605c2e9c45b0ebd7d042914a9992a10ae5fef564582a8e5cfd'),
        User(3, 'email3@email.com', 'scrypt:32768:8:1$apjurr0BybKD5iFD$18e78d03cbff3c49feb56ff2ac934aba6d2cbd0026f1a3fba0a22c3a3cf4c66f6a7f99bca234a74e0bcf4417ada78c2457e09945f47819bf4dbc85b016022e46'),
        User(4, 'email4@email.com', 'scrypt:32768:8:1$SLdsXarTogkK2Lsm$5accedbf4c228a605a4163260d39641834dc259ff0aa4a35cc858cfa8575d3896aa68286a9015062e0015a5d77653a50ab2a427c009bc6a2e84f7e694f849daf')
    ]


""" 
When I create a new user, it is successfully added to the user table with the correct hash
""" 

def test_create_new_user_with_hash(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    password = "testing**"
    hash = generate_password_hash(password)
    repository.create_new_user(User(None, 'email5@email.com', hash))

    result = repository.all()
    assert result == [
User(1, 'blob@hotmail.com', 'scrypt:32768:8:1$M60JBIdOoYHi08nh$137a9beb34d68195ddf14648e2f56a4763e5514ddda166c8f24b8a19a439e8eea76693c056dfe379652210637a5cd31cd334e642773518dbb20cf4554cf80322'),
        User(2, 'email2@hotmail.com', 'scrypt:32768:8:1$VHIoPXPuUnh06Q0z$03481d7e4881aa6d4ec6536fb3b237eb31f5d6a295c40ec91018232c08e63e1d7134711f07012f605c2e9c45b0ebd7d042914a9992a10ae5fef564582a8e5cfd'),
        User(3, 'email3@email.com', 'scrypt:32768:8:1$apjurr0BybKD5iFD$18e78d03cbff3c49feb56ff2ac934aba6d2cbd0026f1a3fba0a22c3a3cf4c66f6a7f99bca234a74e0bcf4417ada78c2457e09945f47819bf4dbc85b016022e46'),
        User(4, 'email4@email.com', 'scrypt:32768:8:1$SLdsXarTogkK2Lsm$5accedbf4c228a605a4163260d39641834dc259ff0aa4a35cc858cfa8575d3896aa68286a9015062e0015a5d77653a50ab2a427c009bc6a2e84f7e694f849daf'),
        User(5, 'email5@email.com', hash)
    ]
    assert check_password_hash(hash, password) == True

""" 
When I search for a single user, their email can be located and returned.
""" 
    
def test_find_user(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    user = repository.find_user('email3@email.com')
    assert user == User(3, 'email3@email.com', 'scrypt:32768:8:1$apjurr0BybKD5iFD$18e78d03cbff3c49feb56ff2ac934aba6d2cbd0026f1a3fba0a22c3a3cf4c66f6a7f99bca234a74e0bcf4417ada78c2457e09945f47819bf4dbc85b016022e46')

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
    seed_file_path = 'seeds/blueberries_bnb.sql'
    db_connection.seed(seed_file_path)
    repository = UserRepository(db_connection)
    result = repository.check_email_exists('email7@email.com')
    assert result == False


# '''
# When a password is provided, and it is a valid password with 8 or more characters, 
# it will return a message that it is valid
# '''

# def test_check_password_valid_password(db_connection):
#     db_connection.seed("seeds/blueberries_bnb.sql")
#     repository = UserRepository(db_connection)
#     result = repository.check_password_valid('blobsdf1%')
#     assert result == True



# '''
# When a incorrect length password is provided, it return false
# that the password needs to be at least 8 characters long and has to contain one of the special characters 

# '''

# def test_check_password_invalid_length_password(db_connection):
#     db_connection.seed("seeds/blueberries_bnb.sql")
#     repository = UserRepository(db_connection)
#     result = repository.check_password_valid('23tyd%')
#     assert result ==  False


# '''
# When an invalid password which does not contain any of the special characters is provided,
# it will return false 
# '''

# def test_check_password_no_specials_char(db_connection):
#     db_connection.seed("seeds/blueberries_bnb.sql")
#     repository = UserRepository(db_connection)
#     result = repository.check_password_valid('23tydsdsd')
#     assert result == False

# '''
# when a password is provided that has apostrophes but it is a valid password
# it will return false
# '''
# def test_check_password_apostrophe_specials_char(db_connection):
#     db_connection.seed("seeds/blueberries_bnb.sql")
#     repository = UserRepository(db_connection)
#     result = repository.check_password_valid('"dfsdfdfdf54')
#     assert result == False