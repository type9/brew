import os
import flask
import flask_login
import json

import requests
from bson.objectid import ObjectId
from flask import Flask, Response, render_template, request, redirect, url_for, session, escape
from pymongo import MongoClient
from recommender import Recommender

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Brew')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
users = db.users
flavors = db.flavors

num_recommendations = 15
cocktaildb_drinkurl = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i='
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
    session['username'] = request.form['username'] # login then redirects to index after registering
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
      current_user = users.find_one({'username': session['username']})

      reviews = current_user['reviews']
      recommender = Recommender(reviews)
      recommender.get_recommendations(num_recommendations)
      drink_list = list()
      for i in range(len(recommender.recommendations)):
        r = requests.get(cocktaildb_drinkurl + recommender.recommendations[i][0]) # gets drink object of each drink
        drink = json.loads(r.content)
        drink_list.append(drink[0])
      print(recommender.recommendations)
      return render_template('home.html', drink_list=drink_list)

    return redirect(url_for('login'))
  
@app.route('/', methods=['POST'])
def add_review():
  current_user = users.find_one({'username': session['username']})

  db_action = '$push'
  action_index = 0
  for review in current_user['reviews']: # this code sees if a review on the drink already exists
    if review['drink_id'] == request.form['drink_id']:
      db_action = '$set'
      break
    action_index += 1 # uses to find the index that needs to be changed if action is 'set'
  
  if db_action == '$push':
    users.update_one( # updates or pushes a review
      { 'username': session['username'] },
      {
        db_action: {
          'reviews': {
            'drink_id': request.form['drink_id'], 
            'preference': request.form['preference']
          }
        }
      }
    )
  elif db_action == '$set':
    print(str(action_index))
    users.update_one( # updates or pushes a review
      {'username': session['username']}, {
        db_action: {'reviews.' + str(action_index) + '.preference': request.form['preference']}}
    )
  return redirect(url_for('index'))
  
@app.route('/reviews')
def view_reviews():
  current_user = users.find_one({'username': session['username']})

  print(current_user['reviews'])
  return render_template('review_index.html', review_list=current_user['reviews'])

@app.route('/delete_review/<drink_id>', methods=['POST'])
def delete_review(drink_id):
  users.update_one( # pulls review and removes it from reviews
    { 'username': session['username'] },
    { '$pull': { 'reviews': { 'drink_id': drink_id } } }
  )
  return redirect(url_for('view_reviews'))
  

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))