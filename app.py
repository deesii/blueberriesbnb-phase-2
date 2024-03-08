import os
from flask import Flask, request, render_template, session
from flask_session import Session
from lib.database_connection import get_flask_database_connection
from lib.property_repository import PropertyRepository
from lib.property import Property
from lib.user_repository import UserRepository
from lib.user import User

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index

@app.route('/register', methods = ['POST', 'GET'])
def get_registration_page():
    if request.method == 'POST':
        email_from_form = request.form.get('email')
        if email_from_form:
            # connection = get_flask_database_connection(app)
            # repository = UserRepository(connection)
            # new_user = User(None, email=email_from_form) 
            # if repository.check_email_exists(new_user) == "Please create an account!":
            #     repository.create_new_user(new_user)
            return render_template('successful_registration.html', email=email_from_form)
            # else:
            #     return "Email has already been registered!"
            
        else:
            return "Email is required for registration"

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
def login():
    return render_template('login.html')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
