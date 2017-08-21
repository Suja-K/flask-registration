from flask import render_template, request, redirect, url_for
from flask_login import login_user
from app.home import home
from app import mongo, bcrypt, login_manager


@home.route('/')
def start():
    return render_template('index.html')


@home.route('/sign')
def sign():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if mongo.db.users.find_one({'email': email}):
            if password == bcrypt.check_password_hash(password):
                mongo.db.users.update({'email': email}, {'$set': {'authenticated': True}})
                login_user(user=email)
                return redirect(url_for('user.profile'))
            else:
                print('Incorrect Credentials')
        else:
            return redirect(url_for('home.register'))
    return render_template('home/sign.html')


@home.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if mongo.db.users.find_one({'email': email}):
            return redirect(url_for('home.sign'))
        else:
            mongo.db.users.insert({'email': email, 'password': bcrypt.generate_password_hash(password), 'authenticated': False})
            return redirect(url_for('home.sign'))
    return render_template('home/register.html')
