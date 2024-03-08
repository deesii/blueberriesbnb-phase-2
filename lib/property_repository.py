from lib.property import Property

class PropertyRepository:
    def __init__ (self, connection):
        self._connection = connection

    def all (self):
        rows = self._connection.execute("SELECT * FROM properties")
        properties = []
        for row in rows:
            property = Property(row["id"], row["property_name"], row["user_id"], row["description"], row["price_per_night"])
            properties.append(property)
        return properties

    def add(self, property):

        rows = self._connection.execute("INSERT INTO properties (property_name, user_id, description, price_per_night) VALUES (%s, %s, %s, %s)", [
            property._property_name,
            property._user_id,
            property._description,
            property._price_per_night])
        
        return None
        

    def find_property_by_user_id(self, user_id):
        
        rows = self._connection.execute("SELECT * FROM properties WHERE user_id = %s", [user_id])
        print (rows)
        properties = []
        for row in rows:
            property = Property(row["id"], row["property_name"], row["user_id"], row["description"], row["price_per_night"])
            properties.append(property)
        
        return properties
    

    def find_property_by_id(self, id):
    
        rows = self._connection.execute("SELECT * FROM properties WHERE id = %s", [id])
        print (rows)
        properties = []
        for row in rows:
            property = Property(row["id"], row["property_name"], row["user_id"], row["description"], row["price_per_night"])
            properties.append(property)
        try:
            return properties[0]
        except(IndexError):
            return "property not found"