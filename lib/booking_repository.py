from lib.booking import Booking
from datetime import datetime
import pandas as pd


class BookingRepository():
    def __init__(self, connection):
        self._connection = connection
        

    def list_booking_by_id(self, id):
        rows = self._connection.execute("SELECT * FROM bookings WHERE id = %s", (id,))
        bookings_list = []
        for row in rows:
            booking = Booking(row['id'], row['property_id'], row['dates_booked_from'], row['dates_booked_to'], row['approved'], row['booker_id'])
            bookings_list.append(booking)
        
        if not bookings_list:
            return f"No booking found with ID: {id}"
        
        return bookings_list

    def create_booking(self, booking):
        self._connection.execute('INSERT INTO bookings (property_id, dates_booked_from, dates_booked_to, approved, booker_id) VALUES (%s, %s, %s, %s, %s)',
    [
        booking.property_id,
        booking.dates_booked_from,
        booking.dates_booked_to,
        booking.approved,
        booking.booker_id
    ]
)
    
    def show_user_bookings(self, booker_id):
        rows = self._connection.execute("SELECT * FROM bookings WHERE booker_id = %s", (booker_id,))

        user_bookings = []
        for row in rows:
            booking = Booking(row['id'], row['property_id'], row['dates_booked_from'], row['dates_booked_to'], row['approved'], row['booker_id'])
            user_bookings.append(booking)
        return user_bookings
        
    def show_property_bookings(self,property_id):
        rows = self._connection.execute("SELECT * FROM bookings WHERE property_id = %s", (property_id,))
        property_bookings = []
        for row in rows:
            booking = Booking(row ['id'], row['property_id'], row['dates_booked_from'], row['dates_booked_to'], row['approved'], row['booker_id'])
            property_bookings.append(booking)
        return property_bookings
    

    def change_booking_approval(self, id):
        self._connection.execute("UPDATE bookings SET approved = 'TRUE' WHERE id = %s" , (id,))
        return None
    
    def dates_taken(self, property_id):
        bookings = self.show_property_bookings(property_id)
        dates_taken = []
        for booking in bookings:
            if booking.approved:
                dates_taken += self._dates_in_range(booking.dates_booked_from, booking.dates_booked_to)
        return dates_taken

    def _dates_in_range(self, date_from, date_to=None):
        if not date_to:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
            return [date_from.strftime("%d/%m/%Y")]

        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        
        timestamps = pd.date_range(date_from, date_to).tolist()
        return [timestamp.strftime("%d/%m/%Y") for timestamp in timestamps]







    


