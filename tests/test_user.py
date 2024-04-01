from lib.user import User


""" 
When I construct a user 
With the fields id , email, and password
They are reflected in the instance properties
"""

def test_constructs_with_fields():
    user = User(1,'blob@hotmail.com', 'testing0')
    assert user.email == 'blob@hotmail.com'
    assert user.password == 'testing0'


def test_users_format_nicely():
    user = User(1, 'blob@hotmail.com', 'testing0')
    assert str(user) == "User(blob@hotmail.com, testing0)"
    # Try commenting out the `__repr__` method in lib/artist.py
    # And see what happens when you run this test again.

"""
We can compare two identical artists
And have them be equal
"""
def test_users_are_equal():
    user1 = User(6, "Test email", "testing0")
    user2 = User(6, "Test email", "testing0")
    assert user1 == user2