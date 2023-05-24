from app import db

from models.models import Login
from models.models import Player
from models.models import UserPermission
from models.models import Users


def user_signup(request):
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and \
            'email' in request.form:
        username = request.form['username']
        email = request.form['email']

        # Check if user already exists in db:
        login_user = Login.query.get(username)
        user_exists = Users.query.filter_by(email=email).first()
        if login_user:
            if user_exists:
                if user_exists.email == email:  # username and email found in db
                    msg = 'User exists, Try Logging in?'
            else:  # Someone has that username already
                msg = 'Sorry, that username is taken. Try another?'
        elif user_exists:  # Username is incorrect, but the email exists in db
            msg = 'User exists, Try Logging in?'
        else:
            success_bool = create_new_account(request)
            if success_bool:
                msg = 'You have successfully registered !'
    return msg


def create_new_account(request):
    # Insert into Login
    db.session.add(Login(login_id=request.form['username'], password=request.form['password']))

    # Insert into user
    db.session.add(
        Users(first_name=request.form['firstname'], email=request.form['email'], last_name=request.form['lastname'],
              login_id=request.form['username']))
    db.session.commit()

    # Insert into UserPermission
    db.session.expire_all()
    user_table_id = Users.query.filter_by(email=request.form['email']).first().id
    db.session.add(
        Player(player_id=user_table_id, social_media_consent=True, competing_gender=request.form['gender_optionsRadios'].upper()))
    db.session.add(
        UserPermission(user_id=user_table_id, permission_id=2))
    db.session.commit()

    db.session.expire_all()

    return True
