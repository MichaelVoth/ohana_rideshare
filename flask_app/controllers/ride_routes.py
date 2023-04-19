from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.rides import Ride
from flask_app.models.messages import Message


@app.route('/dashboard')
def dashboard_page():
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')
    # Gets user info by id in session.
    user = User.get_by_id({'id': session['user_id']})
    driverless_rides = Ride.get_all_driverless_rides()
    rides = Ride.get_all_rides()

    return render_template('dashboard.html', user=user, driverless_rides=driverless_rides, rides=rides)


@app.route('/create')
def create_ride():
    # Checks if user id is logged in.
    if session.get('user_id') is None:
        return redirect('/')

    return render_template('create.html')


@app.route('/add/ride', methods=['POST'])
def add_ride():
    if session.get('user_id') is None:
        return redirect('/')

    # Handles validation of creation.
    if not Ride.validate_ride(request.form):
        return redirect('/create')

    # Saves user in DB.
    Ride.save(request.form)

    return redirect("/dashboard")


@app.route('/add/driver', methods=['POST'])
def add_a_driver():
    if session.get('user_id') is None:
        return redirect('/')
    
    data = {
        'id': session['user_id'],
        'ride_id': request.form['id']
    }
    Ride.save_driver(data)
    
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show_ride(id):
    if session.get('user_id') is None:
        return redirect('/')
    
    ride = Ride.get_ride_by_id(id)
    messages = Message.get_messages(id)

    return render_template('show.html', ride=ride, messages=messages)



@app.route('/edit/<int:id>')
def edit_ride(id):
    if session.get('user_id') is None:
        return redirect('/')
    
    ride = Ride.get_ride_by_id(id)

    return render_template('edit.html', ride=ride)


@app.route('/edit/process', methods=['POST'])
def update_ride():
    if session.get('user_id') is None:
        return redirect('/')
    
    Ride.update_ride_info(request.form)

    return redirect('/dashboard')


@app.route('/cancel/<int:id>')
def cancel_driver(id):
    if session.get('user_id') is None:
        return redirect('/')
    
    Ride.remove_driver(id)

    return redirect('/dashboard')



@app.route('/delete/<int:id>')
def delete_ride(id):
    if session.get('user_id') is None:
        return redirect('/')

    Ride.delete_ride(id)
    return redirect('/dashboard')