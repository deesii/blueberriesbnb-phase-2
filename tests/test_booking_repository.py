from lib.booking import *
from lib.booking_repository import *
import pytest

'''
When requested, a booking by id is shown
'''

def test_show_requested_booking_by_id(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    result = repository.list_booking_by_id(4)
    assert result == [
        Booking(4, 3, '2024-05-01', '2024-05-10', False, 4),
    ] 


'''
When there is no booking for the requested id an error message is retrieved
'''

def test_error_no_booking_found(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    error_result = repository.list_booking_by_id(6)
    assert error_result  == "No booking found with ID: 6"


"""
Given a property and dates, a booking can be stored in the table
"""
def test_create_booking(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)

    repository.create_booking(Booking(None, 3,'2024-08-01', '2024-08-02', True, 4,))
    result = repository.show_user_bookings(4)
    assert result == [
        Booking(2, 3, '2024-07-01', '2024-07-10', True, 4),
        Booking(3, 3, '2024-06-01', '2024-06-10', True, 4),
        Booking(4, 3, '2024-05-01', '2024-05-10', False, 4),
        Booking(5, 3, '2024-08-01', '2024-08-02', True, 4)
    ] 

"""
When requested, all bookings for a user are shown
"""
def test_show_user_bookings(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)

    result = repository.show_user_bookings(2)
    assert result == [
    Booking(1, 1, '2024-03-27', '2024-03-29', True, 2)
]

"""
When requested, all bookings for a property are shown
"""
def test_show_property_bookings(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    result = repository.show_property_bookings(3)
    assert result == [
        Booking(2, 3, '2024-07-01', '2024-07-10', True, 4),
        Booking(3, 3, '2024-06-01', '2024-06-10', True, 4),
        Booking(4, 3, '2024-05-01', '2024-05-10', False, 4)
    ]

"""
When requested, the booking for a property has changed from false to true and this is reflected when calling the id.
"""
def test_approval_booking(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    id_to_test = 4
    repository.change_booking_approval(id_to_test)
    result = repository.list_booking_by_id(id_to_test)
    assert result  == [
        Booking(4, 3, '2024-05-01', '2024-05-10', True, 4)
    ]

def test_dates_taken(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    dates = repository.dates_taken(1)
    # assert dates == [
    #     "27/03/2024",
    #     "28/03/2024",
    #     "29/03/2024"
    # ]
    
def test_dates_in_range(db_connection):
    db_connection.seed("seeds/blueberries_bnb.sql")
    repository = BookingRepository(db_connection)
    dates = repository.dates_in_range("2024-03-27", "2024-03-29")
    assert dates == [
        "27/03/2024",
        "28/03/2024",
        "29/03/2024"
    ]
    assert repository.dates_in_range("2024-03-27") == ["27/03/2024"]


