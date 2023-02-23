from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users_model import User


@app.route('/')
def index():

    return redirect('/log_in_register')


@app.route('/log_in_register')
def log_in_register():

    return render_template('home.html')




@app.route('/dashboard')
def dashboard():
    if 'uid' in session:
        user_logged_in = User.get_one(session['uid'])
        return render_template('dashboard.html', user=user_logged_in)
    
    flash("Access denied, Please log-in", 'invalid_Login')
    return redirect('/')



@app.route('/register-user', methods=['POST'])
def create_user():

    if not User.validate(request.form):
        return redirect('/')

    user_id = User.create(request.form)
    
    
    session['uid'] = user_id
    
    

    return redirect('/dashboard')




@app.route('/login', methods=['POST'])
def log_in():

    logged_in_user = User.validate_login(request.form)
    if not logged_in_user:
        return redirect('/')

    session['uid'] = logged_in_user.id

    return redirect('/dashboard')


@app.route('/log_out')
def log_out():
    session.clear()

    return redirect('/')
