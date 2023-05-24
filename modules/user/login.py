from flask import session
from models.models import Login, Users

'''
This file contains functions that manage player signin and signup
'''


def user_signin(request):
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        # Get user from db
        login_user = Login.query.get(username)

        if login_user:
            correct_password = login_user.password
            if password == correct_password:
                session['logged_in'] = True
                user_obj = Users.query.filter_by(login_id=username).first()
                session['user_id'] = user_obj.id
                return True, 'Logged in'
            elif password != correct_password:
                return False, 'Incorrect username / password'
        else:
            return False, 'No account found,check username or please sign up'
    return False, ''



