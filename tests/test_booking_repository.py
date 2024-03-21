from lib.booking import *
from lib.booking_repository import *

"""
Given a property and dates, a booking can be stored in the table
"""
def test_create_booking(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)

    repository.create_booking(Booking(3,'2024-08-01', '2024-08-02', True, 4,))
    result = repository.show_user_bookings(4)
    assert result == [
        Booking(3, '2024-07-01', '2024-07-10', True, 4),
        Booking(3, '2024-06-01', '2024-06-10', True, 4),
        Booking(3, '2024-05-01', '2024-05-10', False, 4),
        Booking(3, '2024-08-01', '2024-08-02', True, 4)
    ] 

"""
When requested, all bookings for a user are shown
"""
def test_show_user_bookings(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)

    result = repository.show_user_bookings(2)
    assert result == [
    Booking(1, '2024-03-27', '2024-03-29', True, 2)
]

"""
When requested, all bookings for a property are shown
"""
def test_show_property_bookings(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    result = repository.show_property_bookings(3)
    assert result == [
        Booking(3, '2024-07-01', '2024-07-10', True, 4),
        Booking(3, '2024-06-01', '2024-06-10', True, 4),
        Booking(3, '2024-05-01', '2024-05-10', False, 4)
    ]