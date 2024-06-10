# MakersBnB Team Blueberry

This is the continuation of the MakersBnB project, which started as part of the Makers Academy Software Engineering Bootcamp.

## Setup

```shell
# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Install the virtual browser we will use for testing
; playwright install
# If you have problems with the above, contact your coach

# Create a test database
; createdb BLUEBERRIES_BnB_TEST 

# Open lib/database_connection.py and change the database names
; open lib/database_connection.py


```

# environmental variables

create .env file in project root directory with the following environmental variables 

If there is no user password set:

    DB_URL=postgresql://localhost/BLUEBERRIES_BnB_TEST 



```shell

# exit out of the virtual environment
; exit

# Re-install dependencies and set up the virtual environment
; pipenv install

# Run the tests (with extra logging)
; pytest -sv

# Run the app
; python app.py

# Now visit http://localhost:5001 in your browser
```
