from lib.booking import Booking

""" 
When I construct a user 
With the fields id and email
They are reflected in the instance properties
"""

def test_constructs_with_fields():
    booking = Booking(1, 1, '2024-03-27', '2024-03-29', True, 2)
    assert booking.id == 1
    assert booking.property_id == 1
    assert booking.dates_booked_from == '2024-03-27'
    assert booking.dates_booked_to == '2024-03-29'
    assert booking.approved == True
    assert booking.booker_id == 2


def test_users_format_nicely():
    booking = Booking(1, 1, '2024-03-27', '2024-03-29', True, 2)
    assert str(booking) == "Booking(1, 1, 2024-03-27, 2024-03-29, True, 2)"
    # Try commenting out the `__repr__` method in lib/artist.py
    # And see what happens when you run this test again.

"""
We can compare two identical artists
And have them be equal
"""
def test_users_are_equal():
    booking1 = Booking(1, 1, "test_date_from", "test_date_to", True, 2)
    booking2 = Booking(1, 1, "test_date_from", "test_date_to", True, 2)
    assert booking1 == booking2