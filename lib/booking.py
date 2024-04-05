
class Booking():
    def __init__(self, id, property_id, dates_booked_from, dates_booked_to,approved,booker_id):
        self.id = id
        self.property_id = property_id
        self.dates_booked_from = dates_booked_from
        self.dates_booked_to = dates_booked_to
        self.approved = approved
        self.booker_id = booker_id

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__
    

    def __repr__(self):
        return f"Booking({self.id}, {self.property_id}, {self.dates_booked_from}, {self.dates_booked_to}, {self.approved}, {self.booker_id})"


