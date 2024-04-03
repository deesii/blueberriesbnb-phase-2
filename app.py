import os
from flask import Flask, request, render_template, session, redirect
from flask_session import Session
from lib.database_connection import get_flask_database_connection
from lib.property_repository import PropertyRepository
from lib.property import Property
from lib.user_repository import UserRepository
from lib.user import User
from lib.booking_repository import BookingRepository
from lib.booking import Booking
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

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

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function




@app.route('/register', methods = ['POST', 'GET'])
def get_registration_page():
    """
    Form for user registration
    """
    if request.method == 'POST':
        email_from_form = request.form.get('email')
        password_from_form = request.form.get('password')
        if not email_from_form or not password_from_form:
            return 'You need all inputs to be filled in!', 400
        else:
            connection = get_flask_database_connection(app)
            repository = UserRepository(connection)
            if repository.check_email_exists(email_from_form) == True:
                return "Email has already been registered"
            else:
                special_characters = '!@$%^&#~;:><=+-'
                password_special_char = [char for char in special_characters if char in password_from_form]
                password_valid = len(password_from_form) >= 8 and len(password_special_char) > 0
                if password_valid:
                        hash_password = generate_password_hash(password_from_form)
                        new_user = User(None, email_from_form, hash_password) 
                        repository.create_new_user(new_user)
                else:
                    return '''Password must contain at least 8 characters and include 
                    one of the following characters !@$%^&#~;:><=+- '''
            return render_template('successful_registration.html', email=email_from_form)

    else:
        return render_template('register.html')


@app.route('/', methods=['GET'])
def get_properties():
    """
    Index page to show list of properties available
    """
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    properties = repository.all()
    print(properties)
    return render_template('index.html', properties=properties), 200

@app.route('/properties/<int:id>', methods=['GET'])
def show_property_by_id(id):
    """
    Page to show details of individual properties
    Also serves as a booking form for each property
    """
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    property = repository.find_property_by_id(id)
    return render_template('get_property.html', property=property)

@app.route('/properties/<int:id>', methods=['POST'])
def create_booking(id):
    """
    If all details are valid, a property should be booked by filling in the booking form
    """
    if not request.form.get('date_from') or not request.form.get('date_to'):
        return 'One of the inputs is not filled in!', 400
    
    date_from = request.form.get('date_from')
    date_to = request.form.get('date_to')
    booker_id = session.get("user_id")

    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    booking = Booking(
        id,
        date_from,
        date_to,
        False,
        booker_id
    )
    repository.create_booking(booking)
    return redirect("/bookings") , 302
    

@app.route('/bookings', methods=['GET'])
@login_required
def list_bookings():
    connection = get_flask_database_connection(app)
    repository = BookingRepository(connection)
    properties_repository = PropertyRepository(connection)
    try:
        user = session["user_id"]
        bookings = repository.show_user_bookings(user)
        print(bookings)
        
        my_properties = properties_repository.find_property_by_user_id(user)
        print(f"these are my properties : {my_properties}")
        booking_my_properties = {}
        
        #for each property give a list of the bookings, with the key as the property id and value a list of bookings
        for property in my_properties:
            property_id = property._id
            booking_per_property = repository.show_property_bookings(property_id)
            booking_my_properties[property_id] = booking_per_property
        
        print(booking_my_properties)
        
        properties = properties_repository.all()
        booked_properties = []
        
        for booking in bookings:
            # print(booking)
            # print(booking.property_id)
            booking_id_to_find = booking.property_id
            for property in properties:
                if property._id == booking_id_to_find:
                    property_details = {
                        'property_name': property._property_name,
                        'description': property._description,
                        'dates_booked_from': booking.dates_booked_from,
                        'dates_booked_to': booking.dates_booked_to,
                        'price_per_night': property._price_per_night
                    }
                    booked_properties.append(property_details) 
        return render_template('bookings.html', booked_properties = booked_properties, my_properties = my_properties, booking_my_properties = booking_my_properties)
    except KeyError:
        return redirect ("/login") , 302

#show list of properties by user

@app.route('/my_properties' , methods=['GET'])
@login_required
def show_property_by_user_id():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    try:
        user = session["user_id"]
        my_properties = repository.find_property_by_user_id(user)
    #print(my_properties)
        return render_template('my_properties.html', my_properties = my_properties), 200
    except KeyError:
        return redirect('/login'), 302
    

@app.route('/add_property', methods = ['POST'])
@login_required
def add_properties():
    if not request.form.get('property_name') or not request.form.get('description') or not request.form.get('price_per_night'): #'user_id' not in request.form
        return 'One of the inputs is not filled in!', 400
    
    property_name_from_form = request.form.get('property_name')
    description_from_form = request.form.get('description')
    price_per_night_from_form = request.form.get('price_per_night')
    user = session["user_id"]

    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    property = Property(None,
                    property_name_from_form,
                    user,
                    description_from_form,
                    price_per_night_from_form
                    )
    repository.add(property)
    return redirect("/") , 302

@app.route('/add_property', methods=['GET'])
@login_required
def get_add_property_page():

    # if "user_id" not in session:
    #     return render_template("login.html")

    # user = session["user_id"]
    # print(f"the user id is {user}")
    return render_template('adding_property.html')


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

@app.route("/logout")
def logout_user():
    """Log user out"""
    session.clear()

    return redirect("/"), 302
    




# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
