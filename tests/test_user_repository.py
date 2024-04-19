from lib.user_repository import UserRepository
from lib.user import User
from werkzeug.security import check_password_hash,generate_password_hash



def test_correct_hashing_password(db_connection, update_seed_file_with_hashes):
    seed_file_path = 'seeds/blueberries_bnb.sql'
    update_seed_file_with_hashes(seed_file_path)
    db_connection.seed(seed_file_path)
    repository = UserRepository(db_connection)
    user = repository.find_user('blob@hotmail.com')
    assert check_password_hash(user.password, "testing0&") == True
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
        User(1, 'blob@hotmail.com', 'scrypt:32768:8:1$D5hPxJWs7M5vRKiG$c7b58270a7aa94d2c46562cf7997242b2e125b64efc2e606334d6cec4bfa109476cf42834d6c6a2bc3a7e7e731c59652a14ea954d1f565796f6cd47aebd180bf'),
        User(2, 'email2@hotmail.com', 'scrypt:32768:8:1$0oFHlAmpvTynd2Cu$827d8271180250b1c2ac44d0f43c98e5da2bdb85e3b2327cb97386794a5327e1ceeb56b672d2a7dc8f5074d9c7afabfe4526be6f347bf8e83a4acfa762972080'),
        User(3, 'email3@email.com', 'scrypt:32768:8:1$4zgtCgNqq9Xa2XXL$182dcccc5e52fd9d8955b551c171a5de7da0703556bc6e4ebe8a6d21f089645c07d981294bbdc2a6500e8ea4a4a69d02744afb81686fbac214c6be27fe49319f'),
        User(4, 'email4@email.com', 'scrypt:32768:8:1$Lf5XkQnZG1pgvVQX$cfb10e933e3e89deb8838717e44834cf5044edf092829fc46508acbd8ff6d97eb391749ff093fccb05be65e797321d41b2912b77715382640f8812f2b72b8693')
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
    User(1, 'blob@hotmail.com', 'scrypt:32768:8:1$D5hPxJWs7M5vRKiG$c7b58270a7aa94d2c46562cf7997242b2e125b64efc2e606334d6cec4bfa109476cf42834d6c6a2bc3a7e7e731c59652a14ea954d1f565796f6cd47aebd180bf'),
        User(2, 'email2@hotmail.com', 'scrypt:32768:8:1$0oFHlAmpvTynd2Cu$827d8271180250b1c2ac44d0f43c98e5da2bdb85e3b2327cb97386794a5327e1ceeb56b672d2a7dc8f5074d9c7afabfe4526be6f347bf8e83a4acfa762972080'),
        User(3, 'email3@email.com', 'scrypt:32768:8:1$4zgtCgNqq9Xa2XXL$182dcccc5e52fd9d8955b551c171a5de7da0703556bc6e4ebe8a6d21f089645c07d981294bbdc2a6500e8ea4a4a69d02744afb81686fbac214c6be27fe49319f'),
        User(4, 'email4@email.com', 'scrypt:32768:8:1$Lf5XkQnZG1pgvVQX$cfb10e933e3e89deb8838717e44834cf5044edf092829fc46508acbd8ff6d97eb391749ff093fccb05be65e797321d41b2912b77715382640f8812f2b72b8693'),
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
    assert user == User(3, 'email3@email.com', 'scrypt:32768:8:1$4zgtCgNqq9Xa2XXL$182dcccc5e52fd9d8955b551c171a5de7da0703556bc6e4ebe8a6d21f089645c07d981294bbdc2a6500e8ea4a4a69d02744afb81686fbac214c6be27fe49319f')

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


'''
When a password is provided, and it is a valid password with 8 or more characters, 
it will return a message that it is valid
'''

def test_check_password_valid_password(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.check_password_valid('blobsdf1%')
    assert result == True



'''
When a incorrect length password is provided, it return false
that the password needs to be at least 8 characters long and has to contain one of the special characters 

'''

def test_check_password_invalid_length_password(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.check_password_valid('23tyd%')
    assert result ==  False


'''
When an invalid password which does not contain any of the special characters is provided,
it will return false 
'''

def test_check_password_no_specials_char(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.check_password_valid('23tydsdsd')
    assert result == False

'''
when a password is provided that has apostrophes but it is a valid password
it will return false
'''
def test_check_password_apostrophe_specials_char(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = UserRepository(db_connection)
    result = repository.check_password_valid('"dfsdfdfdf54')
    assert result == False