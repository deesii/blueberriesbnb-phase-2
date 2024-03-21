import os
from flask import Flask, request, render_template, session, redirect
from flask_session import Session
from lib.database_connection import get_flask_database_connection
from lib.property_repository import PropertyRepository
from lib.property import Property
from lib.user_repository import UserRepository
from lib.user import User
from lib.booking_repository import BookingRepository

# Create a new Flask app
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
# def login_required(f):
#     """
#     Decorate routes to require login.

#     https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
#     """
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect("/login")
#         return f(*args, **kwargs)
#     return decorated_function




@app.route('/register', methods = ['POST', 'GET'])
def get_registration_page():
    if request.method == 'POST':
        email_from_form = request.form.get('email')
        if email_from_form:
            connection = get_flask_database_connection(app)
            repository = UserRepository(connection)
            if repository.check_email_exists(email_from_form) == False:
                new_user = User(None, email_from_form) 
                repository.create_new_user(new_user)
            else:
                return "Email already exists"
            
            return render_template('successful_registration.html', email=email_from_form)
            # else:
            # #     return "Email has already been registered!"
    
    else:
        return render_template('register.html')

@app.route('/', methods=['GET'])
def get_properties():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
    return render_template('index.html', properties=properties), 200
  

@app.route('/properties/<int:id>', methods=['GET'])
def show_property_by_id(id):
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    property = repository.find_property_by_id(id)
    return render_template('get_property.html', property=property)

@app.route('/bookings', methods=['GET'])
def list_bookings():
    connection=get_flask_database_connection(app)
    repository = BookingRepository(connection)
    return render_template('bookings.html')


@app.route('/add_property', methods = ['POST'])
def add_properties():
    if 'property_name' not in request.form or 'description' not in request.form or 'user_id' not in request.form or 'price_per_night' not in request.form:
        return 'One of the inputs is not filled in!', 400
    
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    property = Property(None,
                    request.form['property_name'],
                    request.form['user_id'],
                    request.form['description'],
                    request.form['price_per_night']
                    )
    repository.add(property)
    return "" , 200 


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login_user():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        # if not request.form.get("email"):
        #     return apology("must provide username", 403)

        # # Ensure password was submitted
        # elif not request.form.get("password"):
        #     return apology("must provide password", 403)

        # Query database for username
        connection = get_flask_database_connection(app)
        repo = UserRepository(connection)
        email = request.form.get("email")

        # Ensure username exists and password is correct
        user = repo.find_user(email)
        try:
            session["user_id"] = user.id
        except AttributeError:
            return redirect("/register")
        
        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
