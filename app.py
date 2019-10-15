import os
import flask
import flask_login

from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from user import User

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Brew')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
# users = db.users
flavors = db.flavors
users = {'foo@bar.tld': {'password': 'secret'}}

app = Flask(__name__)
app.secret_key = 'secret string'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/')
def landing():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' password='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    
    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))
    return 'Bad login'

@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'logged out'

@login_manager.unauthorized_handler
def unauthroized_handler():
    return 'Unauthorized'


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))