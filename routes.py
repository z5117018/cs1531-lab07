from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from server import app, system
from datetime import datetime
from src.Location import Location
from src.Customer import *
from src.CarRentalSystem import *

crs = CarRentalSystem()
c = Customer('user','pass','lic')
system.new_customer(c)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Task 1: complete this function
    """
    if (request.method == 'POST'):
        username = request.form.get('username','')
        password = request.form.get('password','')
        user = system.validate_login(username,password)
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404


@app.route('/cars',methods=['POST','GET'])
@login_required
def cars():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        c = system.car_search(make,model)
        return render_template('cars.html',cars = c)
    """
    Task 2: At the moment this endpoint does not do anything if a search
    is sent. It should filter the cars depending on the search criteria
    """
    cars = system.cars # This line is deleted in the model solution
    return render_template('cars.html', cars=cars)


@app.route('/cars/<rego>')
@login_required
def car(rego):
    car = system.get_car(rego)
    if car is None:
        abort(404)
    return render_template('car_details.html', car=car)


@app.route('/cars/<rego>/book', methods=["GET", "POST"])
@login_required
def book(rego):
    car = system.get_car(rego)
    if car is None:
        abort(404)
    if request.method == 'POST':
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(request.form['start_date'], date_format)
        end_date = datetime.strptime(request.form['end_date'], date_format)
        diff = end_date - start_date
        if 'check' in request.form:
            fee = car.get_fee(diff.days)
            return render_template(
                'booking_form.html',
                confirmation=True,
                form=request.form,
                car=car,
                fee=fee
            )
        elif 'confirm' in request.form:
            location = Location(request.form['start'], request.form['end'])
            booking = system.make_booking(current_user, diff, car, location)
            return render_template('booking_confirm.html', booking=booking)
    return render_template('booking_form.html', car=car)


@app.route('/cars/<rego>/bookings')
@login_required
def car_bookings(rego):
    car = system.get_car(rego)
    bookings = car.get_bookings()
    return render_template('bookings.html', bookings = bookings)
    """
    Task 3: This should render a new template that shows a list of all
    the bookings associated with the car represented by 'rego'
    The bookings.html template is intended for this route
    """
    pass
