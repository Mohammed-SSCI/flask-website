from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
#this file is basically to organize a bunch of URLS

auth=Blueprint('auth', __name__)
#this is basically making a seprate page in the url to login 
#EX: id url is shams.com this route makes it so that if it is shams.com/login it takes you somewhere else
@auth.route('/login', methods=['GET','POST'])
def login():
    #a get request is us getting the information a post is us giving the info 
    if request.method=='POST':
        email= request.form.get('email')
        password=request.form.get('password')
        #this filters all users that have that specific email
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                
                flash('Logged in: Successful', category='success')
                #this logs in the user and makes him stay logged in even if refreshes unless they clear browser or any other stuff
                login_user(user,remember=True)    
                return redirect(url_for('views.home'))       
            else:
                flash('Incorrect password or email please try again', category="Error")
        else:
          flash('Email does not exist', category='Error')
    
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
#makes it so that user must login inorder to access this function
@login_required
def logout():
    
    logout_user()

    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def signup():
    #checking if we are getting a post or a get request
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstname')
        lastName =request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        symbols = {'`','~','!','@','#','$','%','^','&','*','(',')','_','-','+','=','{','[','}','}','|'}

        user=User.query.filter_by(email=email).first()
        user2=User.query.filter_by(password=password1).first()
        if user:
            flash('Email alredy exists', category='Error')
        elif user2:
            flash('Password alredy exists', category='Error')

        elif len(email) < 4:
            flash('Email must be valid', category='Error')
        elif len(firstName)<2:
            flash('Firstname is too short', category='Error')
        elif len(lastName)<2:
            flash('Lastname is too short', category='Error')
        elif len(password1) < 10:
            flash('Passwrod must be atleast 10 characters', category='Error')
        elif not any(char.isdigit() for char in password1):

            flash('Password should have at least one number', category='Error')
        elif not any(char.isupper() for char in password1):

            flash('Password should have at least one uppercase letter', category='Error')
        elif not any(char.islower() for char in password1):

            flash('Password should have at least one lowercase letter', category='Error')
        elif not any(char in symbols for char in password1):

            flash('Password should have at least one of special symbol', category='Error')
        elif password1 != password2:
            flash('Passwords must match', category='Error')
        else:
            #add user to database
            new_user=User(email=email, first_name=firstName,last_name=lastName,  password=generate_password_hash(
                password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account has been created', category='Success')
            login_user(user,remember=True)              
            return redirect(url_for('views.home'))
        


    return render_template("sign_up.html",user=current_user)
