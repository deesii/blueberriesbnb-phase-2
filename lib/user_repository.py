from lib.user import User

class UserRepository():
    
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute("SELECT * FROM users")
        users = []
        for row in rows:
            user = User(row["id"], row["email"])
            users.append(user)
        return users
    
    def create_new_user(self,user):
        self._connection.execute('INSERT INTO users (email) VALUES (%s)',[user.email])
        return None
    
    def find_user(self, email):
        rows = self._connection.execute(f"SELECT * FROM users WHERE email = '{email}'")
        print(f"find methods {rows}")

        try:
            for row in rows:
                return User(row['id'], row['email'])
        except Exception as e:
            print(f"Error: {e}")

    
    def check_email_exists(self,email):
        user_email = email
        if self.find_user(user_email) != None:
            return True
        else:
            return False