from lib.user import User
#from werkzeug.security import check_password_hash, generate_password_hash

class UserRepository():
    
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        users = []
        for row in rows:
            user = User(row["id"], row["email"], row["password"])
            users.append(user)
        return users
    
    def create_new_user(self,user):
        self._connection.execute('INSERT INTO users (email, password) VALUES (%s, %s)',[user.email ,user.password])
        return None
    
    def find_user(self, email):
        rows = self._connection.execute(f"SELECT * FROM users WHERE email = '{email}'")
        print(f"find methods {rows}")

        try:
            for row in rows:
                return User(row['id'], row['email'], row['password'])
        except Exception as e:
            print(f"Error: {e}")

    
    def check_email_exists(self,email):
        user_email = email
        return self.find_user(user_email) != None

        
    def check_password_valid(self, password):
        special_characters = '!@$%^&#~;:><=+-'
        password_special_char = [char for char in special_characters if char in password]
        return len(password) >= 8 and len(password_special_char) > 0
    

