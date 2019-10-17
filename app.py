import os
import flask
import flask_login
import json

from bson.objectid import ObjectId
from flask import Flask, Response, render_template, request, redirect, url_for, session, escape
from pymongo import MongoClient
from recommender import Recommender
from login import RegistrationForm, LoginForm

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Brew')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
users = db.users
flavors = db.flavors

num_recommendations = 10
# test_user = User('metal')
# test_user.add_review('11000', 2)
# test_user.add_review('11002', 1)
# test_user.add_review('11009', 1)
# test_user.add_review('11008', -1)

app = Flask(__name__)
app.secret_key = 'secret string'

# LOGIN ROUTES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else: 
      return '''
      <form method="post">
          <p><input type=text name=username>
          <p><input type=submit value=Login>
      </form>
      '''
  
@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    current_user = {
        'username': request.form.get('username'),
        'reviews': []
    }
    users.insert_one(current_user)
    session['username'] = request.form['username']
    return(url_for('index'))
    
  if 'username' in session: # if already logged in
    return redirect(url_for('index'))
  return '''
      <form method="post">
          <p><input type=text name=username>
          <p><input type=submit value=Register>
      </form>
  '''
  
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
# END LOGIN ROUTES

@app.route('/')
def index():
    if 'username' in session:
      # recommend = Recommender(test_user)
      # drink_recommendations = recommend.get_recommendations(num_recommendations)
      return render_template('home.html')

    return redirect(url_for('login'))
  
@app.route('/', methods=['POST'])
def add_review():
  users.update_one(
    { 'username': session['username'] },
    {
      '$push': {
        'reviews': {
          'drink_id': request.args.get('drink_id'), 'preference': request.args.get('preference')
        }
      }
    }
  )
  return redirect(url_for('index'))
  
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))