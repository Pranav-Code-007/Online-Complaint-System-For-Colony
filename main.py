# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, render_template, flash, redirect, url_for, session  # For Cookies, request,  make_response
from forms import RegistrationForm, LoginForm
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from encrypt import encrypt, decrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '91a80165eabf4597daa8e02eac03600c'
# app.secret_key = b'3q\xf4\x85@hS\xf3n\xa0\xf2\xc1\x04\x83\xae\xf2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
#
db = SQLAlchemy(app)


#
class Citizen(db.Model):
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = encrypt(email)
        self.password = encrypt(password)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', page_name="Home")


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['role'] = form.choice.data
        if form.choice.data == 'Citizen':
            return redirect(url_for('citizen'))
        if form.choice.data == 'Councillor':
            return redirect(url_for('councillor'))
    return render_template('login.html', page_name="Login", form=form)
    ################### FOR COOKIES ONLY ######################################
    # res = make_response(redirect(url_for(form.choice.data.lower())))
    # res.set_cookie('login', 'true')
    # return res
    ############################################################################


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('role', None)
    return redirect('home')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.firstname.data}!', 'success')
        return redirect(url_for('signup'))
    return render_template('signup.html', page_name="Signup", form=form)


@app.route('/account')
def citizen():
    return session_check('citizen_account.html')
    # try:
    #     if session['email']:
    #         return render_template('citizen_account.html', page_name="account")
    # except Exception:
    #     return redirect(url_for('error'))
    # return redirect(url_for('error'))
    ################# FOR COOKIES ONLY #######################
    # if request.cookies.get('login') == 'true':
    #     return render_template('citizen_account.html', page_name="account")
    # return redirect(url_for('error'))
    ##########################################################


@app.route('/account')
def councillor():
    return session_check('councillor_account.html')


@app.route('/error')
def error():
    return render_template('error.html')


def session_check(htmlfile):
    try:
        if session['email']:
            return render_template(htmlfile, page_name="account")
    except Exception:
        return redirect(url_for('error'))
    return redirect(url_for('error'))


if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
