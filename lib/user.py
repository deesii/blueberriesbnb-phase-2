class User():
    def __init__(self, id, email):
        self.email = email
        self.id = id

    def __eq__(self, other):
        if other is None:
            return False
        return self.__dict__ == other.__dict__
    

    def __repr__(self):
        return f"User({self.email})"
