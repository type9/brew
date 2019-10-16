import os
import flask
import flask_login

from bson.objectid import ObjectId
from flask import Flask, Response, render_template, request, redirect, url_for, session, escape
from pymongo import MongoClient
from user import User
from flask_wtf import FlaskForm
from login import RegistrationForm, LoginForm

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Brew')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
users = db.users
flavors = db.flavors

app = Flask(__name__)
app.secret_key = 'secret string'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# # LOGIN ROUTES
# @login_manager.user_loader
# def user_loader(user_id):
#     return User.get_id(user_id)

# @login_manager.request_loader
# def load_user(request):
#     token = request.headers.get('Authorization')
#     if token is None:
#         token = request.args.get('token')

#     if token is not None:
#         username,password = token.split(":") # naive token
#         user_entry = User.get_id(username)
#         if (user_entry is not None):
#             user = User(user_entry[0],user_entry[1])
#             if (user.password == password):
#                 return user
#     return None

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User(request.form.get('username'), request.form.get('password'))
#         if user in users:
#             flask_login.login_user(user)

#         flask.flash('Loggged in successfully.')

#         next = request.args.get('next')
#         return flask.redirect(next or url_for('index'))
#     return render_template('login.html', form=form)

# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     return 'Logged in as: ' + flask_login.current_user.id

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))

# @login_manager.unauthorized_handler
# def unauthroized_handler():
#     return 'Unauthorized'
# # END LOGIN ROUTES

@app.route('/')
def index():
    if 'username' in session:
        return (f'Logged in')
    return render_template('login.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))