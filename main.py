from flask import Flask, render_template, flash, request, redirect, url_for, session
import pymysql
import bcrypt
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your_secret_key'

# Enter your database connection details below
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Welcome$101',
    'db': 'carrental',
    'port': 3306,
}


def create_database_and_table():
    connection = pymysql.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'], port=db_config['port'])
    try:
        with connection.cursor() as cursor:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['db']}")
            # Switch to the database
            cursor.execute(f"USE {db_config['db']}")
        connection.commit()
        print("Database and table created successfully.")
    except pymysql.Error as e:
        print(f"Error creating database and table: {e}")
    finally:
        connection.close()

def connect_db():
    create_database_and_table()
    return pymysql.connect(**db_config)


# Function to check if the user is authenticated
def is_authenticated():
    return 'loggedin' in session

# Function to get the user's role
def get_user_role():
    # In a real application, you would likely retrieve the user's role from a database.
    # For this example, let's assume a user with the role 'admin' has the role 'admin'.
    if 'loggedin' in session and 'role' in session:
        if session['role'] == 'admin':
            return 'admin'
        if session['role'] == 'staff':
            return 'staff'
        elif session['role'] == 'customer':
            return 'customer'
    return None


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        connection = connect_db()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            # Fetch one record and return result
            account = cursor.fetchone()
        connection.close()

        if account is not None:
            password = account["PasswordHash"]
            if bcrypt.checkpw(user_password.encode('utf-8'), password.encode('utf-8')):
                # If account exists in accounts table in our database
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['UserID']
                session['username'] = account['Username']
                # Set the user role in the session (you need to adjust this based on your application)
                session['role'] = account['Role']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesn't exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('role', None)  # Remove the user's role from the session
    # Redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST':
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        connection = connect_db()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesn't exist and the form data is valid, now insert new account into accounts table
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                print(hashed)
                cursor.execute('INSERT INTO users (UserName, PasswordHash, Email, Role) VALUES (%s, %s, %s, %s)', (username, hashed, email, 'customer',))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO customers (UserID,CustomerName,Email) VALUES (%s, %s, %s)', (user_id, username, email,))
                connection.commit()
                print (user_id)
                msg = 'You have successfully registered!'
        connection.close()
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for logged-in users
@app.route('/home')
def home():
    # Check if user is logged in
    if is_authenticated():
        # User is logged in, show them the home page
        return render_template('home.html', username=session['username'],role=get_user_role())
    # User is not logged in, redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for logged-in users
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if is_authenticated():
        user_id = session['id']
        connection = connect_db()

        if request.method == 'POST' and get_user_role() == "customer":
            try:
                # Form submission for updating the customer's profile
                username = request.form['username']
                email = request.form['email']
                address = request.form['address']
                phone = request.form['phone']
                new_password = request.form.get('password')
                
                # Validate the email address
                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address!', 'danger')
                # Validate the phone number
                elif not re.match(r'^\d{10}$', phone):
                    flash('Invalid phone number! Phone number should be a 10-digit number.', 'danger')
                # Check if the new password is at least 6 characters long
                elif new_password and len(new_password) < 6:
                    flash('New password must be at least 6 characters long!', 'danger')
                else:
                    # Check if the user entered a new password
                    if new_password:
                        # Hash the new password before storing it
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                        # Update the user's database
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            cursor.execute('UPDATE users SET UserName = %s, PasswordHash = %s, Email = %s WHERE UserID = %s',
                                           (username, hashed_password, email, user_id,))
                            cursor.execute('UPDATE customers SET CustomerName = %s, Address = %s, Email = %s, PhoneNumber = %s WHERE UserID = %s',
                                           (username, address, email, phone, user_id,))
                            connection.commit()
                            connection.close()
                            flash('Profile updated successfully!', 'success')
                            return render_template('profile.html', account=account, role= get_user_role())
                    else:
                        # Update the user's database without changing the password
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            cursor.execute('UPDATE users SET UserName = %s, Email = %s WHERE UserID = %s',
                                           (username, email, user_id,))
                            cursor.execute('UPDATE customers SET CustomerName = %s, Address = %s, Email = %s, PhoneNumber = %s WHERE UserID = %s',
                                           (username, address, email, phone, user_id,))
                            connection.commit()
                            connection.close()
                            flash('Profile updated successfully!', 'success')
                            return render_template('profile.html', account=account, role= get_user_role())

            except Exception as e:
                flash(f'Error updating profile: {e}', 'danger')

        elif request.method == 'POST' and (get_user_role() == "staff" or get_user_role() == "admin"):
            try: 
                # Form submission for updating staff or admin profile
                username = request.form['username']
                email = request.form['email']
                address = request.form['address']
                phone = request.form['phone']
                new_password = request.form.get('password')
                
                # Validate the email address
                if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address!', 'danger')
                # Validate the phone number
                elif not re.match(r'^\d{10}$', phone):
                    flash('Invalid phone number! Phone number should be a 10-digit number.', 'danger')
                # Check if the new password is at least 6 characters long
                elif new_password and len(new_password) < 6:
                    flash('New password must be at least 6 characters long!', 'danger')
                else:
                    # Check if the user entered a new password
                    if new_password:
                        # Hash the new password before storing it
                        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                        # Update the user's database
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            cursor.execute('UPDATE users SET UserName = %s, PasswordHash = %s, Email = %s WHERE UserID = %s',
                                           (username, hashed_password, email, user_id,))
                            cursor.execute('UPDATE staff SET StaffName = %s, Address = %s, Email = %s, PhoneNumber = %s WHERE UserID = %s',
                                           (username, address, email, phone, user_id,))
                            connection.commit()
                            connection.close()
                            flash('Profile updated successfully!', 'success')
                            return render_template('profile.html', account=account, role= get_user_role())

                    else:
                        # Update the user's database without changing the password
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            cursor.execute('UPDATE users SET UserName = %s, Email = %s WHERE UserID = %s',
                                           (username, email, user_id,))
                            cursor.execute('UPDATE staff SET StaffName = %s, Address = %s, Email = %s, PhoneNumber = %s WHERE UserID = %s',
                                           (username, address, email, phone, user_id,))
                            connection.commit()
                            connection.close()
                            flash('Profile updated successfully!', 'success')
                            return render_template('profile.html', account=account, role= get_user_role())


            except Exception as e:
                flash(f'Error updating profile: {e}', 'danger')

        # Fetch the user's profile data based on their role after the update
        if request.method == 'GET' and get_user_role() == 'customer':
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute('SELECT CustomerName, Email, PhoneNumber, Address FROM customers WHERE UserID = %s', (user_id,))
                account = cursor.fetchone()
                connection.close()
                return render_template('profile.html', account=account, role= get_user_role())

        elif request.method == 'GET' and get_user_role() == 'staff' or get_user_role() == 'admin':
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute('SELECT StaffName, Email, PhoneNumber, Address FROM staff WHERE UserID = %s', (user_id,))
                account = cursor.fetchone()
                connection.close()
                return render_template('profile.html', account=account, role= get_user_role())

        connection.close()
        return render_template('profile.html', account=account, role=get_user_role())

    # User is not logged in, redirect to the login page
    return redirect(url_for('login'))



@app.route('/account_management', methods=['GET', 'POST'])
def account_management():
    if is_authenticated():
        if get_user_role() == 'admin' or get_user_role() == 'staff':
            if request.method == 'POST':
                action = request.form.get('action')
                if action == 'search':
                    # Search for customers or staff members
                    search_query = request.form.get('search_query')
                    customers = search_customers(search_query)
                    staff_members = search_staff_members(search_query)
                    return render_template('account_management.html', customers=customers, staff_members=staff_members)

                elif action == 'add_customer':
                        customer_name = request.form['customer_name']
                        email = request.form['email']
                        address = request.form['address']
                        phone = request.form['phone']

                        add_customer(customer_name, email, address, phone)
                        flash('Customer added successfully!', 'success')

                elif action == 'update_customer':
                        customer_id = request.form.get('customer_id')
                        customer_name = request.form['customer_name']
                        email = request.form['email']
                        address = request.form['address']
                        phone = request.form['phone']
                        
                        # Code to update a customer
                        update_customer(customer_id, customer_name, email, address, phone)
                        flash('Customer updated successfully!', 'success')

                elif action == 'delete_customer':
                        customer_id = request.form.get('customer_id')
                        # Code to delete a customer
                        delete_customer(customer_id)
                        flash('Customer deleted successfully!', 'success')
                
                if action == 'add_staff':
                        staff_name = request.form['staff_name']
                        email = request.form['email']
                        address = request.form['address']
                        phone = request.form['phone']
                       

                        # Code to add a staff member
                        add_staff(staff_name, email, address, phone)
                        flash('Staff member added successfully!', 'success')

                elif action == 'update_staff':
                        staff_id = request.form.get('staff_id')
                        staff_name = request.form['staff_name']
                        email = request.form['email']
                        address = request.form['address']
                        phone = request.form['phone']

                    
                        # Code to update a staff member
                        update_staff(staff_id, staff_name, email, address, phone)
                        flash('Staff member updated successfully!', 'success')

                elif action == 'delete_staff':
                        staff_id = request.form.get('staff_id')
                        # Code to delete a staff member
                        delete_staff(staff_id)
                        flash('Staff member deleted successfully!', 'success')

            # Retrieve customers and staff members to display on the account management page
            customers = get_customers()
            staff_members = get_staff_members()
            return render_template('account_management.html', customers=customers, staff_members=staff_members)

    # User is not logged in or not an staff, redirect to login page or access denied page
    return redirect(url_for('login'))

def search_customers(search_query):
    # Code to search customers based on the search_query
    # Return a list of matching customers
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM customers WHERE CustomerName LIKE %s OR Email LIKE %s', ('%' + search_query + '%', '%' + search_query + '%'))
        customers = cursor.fetchall()
    connection.close()
    return customers

# Replace this with your actual logic to search for staff members in the database
def search_staff_members(search_query):
    # Code to search staff members based on the search_query
    # Return a list of matching staff members
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM staff WHERE StaffName LIKE %s OR Email LIKE %s', ('%' + search_query + '%', '%' + search_query + '%'))
        staff_members = cursor.fetchall()
    connection.close()
    return staff_members

# Replace this with your actual logic to add a customer to the database
def add_customer(customer_name, email, address, phone):
    # Code to add a customer to the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('INSERT INTO customers (CustomerName, Email, Address, PhoneNumber) VALUES (%s, %s, %s, %s)',
                       (customer_name, email, address, phone))
    connection.commit()
    connection.close()

# Replace this with your actual logic to update a customer in the database
def update_customer(customer_id, customer_name, email, address, phone):
    # Code to update a customer in the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('UPDATE customers SET CustomerName = %s, Email = %s, Address = %s, PhoneNumber = %s WHERE CustomerID = %s',
                       (customer_name, email, address, phone, customer_id))
    connection.commit()
    connection.close()

# Replace this with your actual logic to delete a customer from the database
def delete_customer(customer_id):
    # Code to delete a customer from the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('DELETE FROM customers WHERE CustomerID = %s', (customer_id,))
    connection.commit()
    connection.close()

# Replace this with your actual logic to get a list of customers from the database
def get_customers():
    # Code to fetch and return a list of customers from the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM customers')
        customers = cursor.fetchall()
    connection.close()
    return customers

# Replace this with your actual logic to add a staff member to the database
def add_staff(staff_name, email, address, phone):
    # Code to add a staff member to the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('INSERT INTO staff (StaffName, Email, Address, PhoneNumber) VALUES (%s, %s, %s, %s)',
                       (staff_name, email, address, phone))
    connection.commit()
    connection.close()

# Replace this with your actual logic to update a staff member in the database
def update_staff(staff_id, staff_name, email, address, phone):
    # Code to update a staff member in the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('UPDATE staff SET StaffName = %s, Email = %s, Address = %s, PhoneNumber = %s WHERE StaffID = %s',
                       (staff_name, email, address, phone, staff_id))
    connection.commit()
    connection.close()

# Replace this with your actual logic to delete a staff member from the database
def delete_staff(staff_id):
    # Code to delete a staff member from the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('DELETE FROM staff WHERE StaffID = %s', (staff_id,))
    connection.commit()
    connection.close()

# Replace this with your actual logic to get a list of staff members from the database
def get_staff_members():
    # Code to fetch and return a list of staff members from the database
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM staff')
        staff_members = cursor.fetchall() 
    connection.close()
    return staff_members


# http://localhost:5000/dashboard - this will be the dashboard page, only accessible for logged-in users
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if is_authenticated():
        if request.method == 'POST':
            # Check if the request is for adding a new car
            if request.form.get('action') == 'add_car':
                try:
                    car_model = request.form['car_model']
                    registration_number = request.form['registration_number']
                    car_image = request.form['car_image']
                    year = int(request.form['year'])
                    seating_capacity = int(request.form['seating_capacity'])
                    rental_per_day = float(request.form['rental_per_day'])

                    # Perform validation for required fields
                    if not car_model or not car_image:
                        raise Exception("Car model and car image are required fields.")

                    if year < 1900 or year > 9999:
                        raise Exception("Invalid year. Please enter a valid year between 1900 and 9999.")

                    if seating_capacity <= 0:
                        raise Exception("Invalid seating capacity. Please enter a value greater than 0.")

                    if rental_per_day <= 0:
                        raise Exception("Invalid rental per day. Please enter a value greater than 0.")

                    
                    # Connect to the database
                    connection = connect_db()
                    with connection.cursor() as cursor:
                        cursor.execute('INSERT INTO rental_cars (CarModel, RegistrationNumber, Year, SeatingCapacity, RentalPerDay, CarImage) VALUES (%s, %s, %s, %s, %s, %s)',
                            (car_model, registration_number, year, seating_capacity, rental_per_day, car_image))
                        connection.commit()
                        connection.close()
                        flash('Car added successfully!', 'success')
                # Catch any exception and display the error message to the user
                except Exception as e:
                    flash(f'Error adding car: {e}', 'danger')

            # Check if the request is for editing a car
            elif request.form.get('action') == 'edit_car':
                try:
                    car_id = int(request.form['car_id'])
                    car_model = request.form['car_model']
                    registration_number = request.form['registration_number']
                    year = int(request.form['year'])
                    seating_capacity = int(request.form['seating_capacity'])
                    rental_per_day = float(request.form['rental_per_day'])
                    car_image = request.form['car_image']

                    connection = connect_db()
                    with connection.cursor() as cursor:
                        cursor.execute('UPDATE rental_cars SET CarModel = %s, RegistrationNumber = %s, Year = %s, SeatingCapacity = %s, RentalPerDay = %s, CarImage = %s WHERE CarID = %s',
                            (car_model, registration_number, year, seating_capacity, rental_per_day, car_image, car_id))
                        connection.commit()
                        connection.close()
                        flash('Car updated successfully!', 'success')   
                except Exception as e:
                    flash(f'Error updating car: {e}', 'danger')

            # Check if the request is for deleting a car
            elif request.form.get('action') == 'delete_car':
                try:
                    car_id = int(request.form['car_id'])
                    connection = connect_db()
                    with connection.cursor() as cursor:
                        cursor.execute('DELETE FROM rental_cars WHERE CarID = %s', (car_id,))
                        connection.commit()
                        connection.close()
                        flash('Car deleted successfully!', 'success')
                except Exception as e:
                    flash(f'Error deleting car: {e}', 'danger')

        # Fetch all the available rental cars from the database
        connection = connect_db()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
             cursor.execute('SELECT * FROM rental_cars')
             rental_cars = cursor.fetchall()
        connection.close()
        role = get_user_role()
        # Render the  dashboard template and rental car data
        return render_template('dashboard.html', rental_cars=rental_cars,role=role)
    else:
        # User is not authenticated. Redirect to the login page.
        return redirect(url_for('login'))
  
@app.route('/car_details/<int:car_id>')
def car_details(car_id):
    # Fetch car details from the database using the provided car_id
    connection = connect_db()
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('SELECT * FROM rental_cars WHERE CarID = %s', (car_id,))
        car = cursor.fetchone()
    connection.close()

    # Render the car details template with the car data
    return render_template('car_details.html', car=car)


if __name__ == '__main__':
    app.run(debug=True)
