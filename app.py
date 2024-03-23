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
    print(properties)
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
    bookings = repository.show_user_bookings(session["user_id"])
    return render_template('bookings.html', bookings=bookings)


#show list of properties by user

@app.route('/my_properties' , methods=['GET'])
def show_property_by_user_id():
    connection = get_flask_database_connection(app)
    repository = PropertyRepository(connection)
    user = session["user_id"]
    my_properties = repository.find_property_by_user_id(user)
    #print(my_properties)
    return render_template('my_properties.html', my_properties = my_properties)

@app.route('/add_property', methods = ['POST'])
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
