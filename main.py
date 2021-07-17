# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from flask import Flask, render_template, flash, redirect, url_for, session  # For Cookies, request,  make_response
from forms import RegistrationForm, LoginForm, ComplaintForm, Submit
# from flask_session import Session
from typing import Callable
from flask_sqlalchemy import SQLAlchemy
from encrypt import encrypt, decrypt
from datetime import date

app = Flask(__name__)

app.config['SECRET_KEY'] = '91a80165eabf4597daa8e02eac03600c'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = b'3q\xf4\x85@hS\xf3n\xa0\xf2\xc1\x04\x83\xae\xf2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable


db = MySQLAlchemy(app)


class Database:
    @staticmethod
    def getName(table, key: str):
        list = table.query.filter_by(email=key).all()
        return list[0].name

    @staticmethod
    def isUserExist(table, email: str):
        list = table.query.filter_by(email=email).first()
        if list is None:
            return False
        return True

    @staticmethod
    def isPasswordCorrect(table, email: str, password):
        list = table.query.filter_by(eamil=email).first()
        return list[0].password == password

    @staticmethod
    def addCitizen(firstname, lastname, email, password):

        db.session.add(Citizen(firstname, lastname, email, password))
        db.session.commit()


    @staticmethod
    def addComplaint(text_compalaint, subject):
        db.session.add(Citizen(text_complaint, subject))
        db.session.commit()


    @staticmethod
    def retrieveComplaints():
        Complaints.query.all()


    @staticmethod
    def deleteAllComplaints():
        db.session.query(Complaints).delete()
        db.session.commit()




class Citizen(db.Model):
    __tablename__ = 'Citizen'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    relationship = db.relationship('Complaints', backref='citizen', uselist=False)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = encrypt(email)
        self.password = encrypt(password)

    def __repr__(self):
        return f'email :{decrypt(self.email)} , password :{decrypt(self.password)}'


class Complaints(db.Model):
    __tablename__ = 'Complaints'
    id = db.Column(db.Integer, db.ForeignKey('Citizen.id'), nullable=False)
    complaint = db.Column(db.String(500), unique=True, nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, complaint, subject)
        self.complaint = complaint
        self.date = date.today()
        self.subject = subject

    def __repr__(self):
        return f' subject :{self.subject} , complaint :{self.complaint} , date :{self.date}'




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
        #
        if form.choice.data == 'Citizen' and Database.isUserExist(Citizen,
                                                                  form.email.data) and Database.isPasswordCorrect(
                Citizen, form.email.data):
            return redirect(url_for('citizen'))
        if form.choice.data == 'Councillor' and Database.isUserExist(Councillor,
                                                                     form.email.data) and Database.isPasswordCorrect(
                Councillor, form.email.data):
            return redirect(url_for('councillor'))
        else:
            flash(f'{form.firstname.data}\'s account does not exist! or maybe the email or password is wrong', 'danger')

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
        if not Database.isCitizenExist(Citizen, form.email.data):
            flash(f'Account created successfully for {form.firstname.data}!', 'success')
            return redirect(url_for('signup'))
        else:
            flash(f'Account for {form.firstname.data} already exists!', 'danger')
    return render_template('signup.html', page_name="Signup", form=form)


@app.route('/account', methods=['POST', 'GET'])
def citizen():
    form = ComplaintForm()
    if session_check():
        if form.validate_on_submit():
            # form.complaint.data
            ############ store the complaint and subject to database #############
            Database.addComplaint(form.complaint.data, form.subject.data)
            flash(f'Your complaint has been submitted', 'success')
        return render_template('citizen_account.html', page_name="account", form=form,
                               date=str(date.today()).split('-')[::-1])

        # try: 'citizen_account.html'
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


@app.route('/councillor')
def councillor():
    submit = Submit()
    if session_check():
        if submit.validate_on_submit():
            Database.deleteAllComplaints()
        return render_template('councillor_account.html', page_name="account", data=Database.retrieveComplaints(),
                               submit=submit)


@app.route('/error')
def error():
    return render_template('error.html')


def session_check():
    try:
        if session['email']:
            return True
    except Exception:
        return redirect(url_for('error'))
    return redirect(url_for('error'))


if __name__ == '__main__':
    app.run(debug=True)
