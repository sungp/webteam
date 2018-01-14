from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from functools import wraps
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item 
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from datetime import datetime

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
  state = ''.join(random.choice(string.ascii_uppercase + string.digits)
      for x in xrange(32))
  login_session['state'] = state
  # return "The current session state is %s" % login_session['state']
  return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
  # Validate state token
  if request.args.get('state') != login_session['state']:
    response = make_response(json.dumps('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  
  # Obtain authorization code
  code = request.data

  try:
    # Upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(
    json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Check that the access token is valid.
  access_token = credentials.access_token
  url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
      % access_token)
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1])
  # If there was an error in the access token info, abort.
  if result.get('error') is not None:
    response = make_response(json.dumps(result.get('error')), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Verify that the access token is used for the intended user.
  gplus_id = credentials.id_token['sub']
  if result['user_id'] != gplus_id:
    response = make_response(
      json.dumps("Token's user ID doesn't match given user ID."), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Verify that the access token is valid for this app.
  if result['issued_to'] != CLIENT_ID:
    response = make_response(
      json.dumps("Token's client ID does not match app's."), 401)
    print "Token's client ID does not match app's."
    response.headers['Content-Type'] = 'application/json'
    return response

  stored_access_token = login_session.get('access_token')
  stored_gplus_id = login_session.get('gplus_id')
  if stored_access_token is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps('Current user is already connected.'),
       200)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Store the access token in the session for later use.
  login_session['access_token'] = credentials.access_token
  login_session['gplus_id'] = gplus_id

  # Get user info
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token': credentials.access_token, 'alt': 'json'}
  answer = requests.get(userinfo_url, params=params)

  data = answer.json()

  login_session['username'] = data['name']
  login_session['picture'] = data['picture']
  login_session['email'] = data['email']
  # ADD PROVIDER TO LOGIN SESSION
  login_session['provider'] = 'google'

  # see if user exists, if it doesn't make a new one
  user_id = getUserID(data["email"])
  if not user_id:
    user_id = createUser(login_session)
  login_session['user_id'] = user_id
  output = ''
  output += '<h1>Welcome, '
  output += login_session['email']
  output += '!</h1>'
  output += '<img src="'
  output += login_session['picture']
  output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
  flash("you are now logged in as %s" % login_session['username'])
  print "done!"
  return output


# User Helper Functions
def createUser(login_session):
  newUser = User(name=login_session['username'], 
      email=login_session['email'], picture=login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email=login_session['email']).one()
  return user.id


def getUserInfo(user_id):
  user = session.query(User).filter_by(id=user_id).one()
  return user


def getUserID(email):
  try:
    user = session.query(User).filter_by(email=email).one()
    return user.id
  except:
    return None

def getCategory(name):
  try:
    category = session.query(Category).filter_by(name = name).one()
    return category 
  except:
    return None

def getItems(category_name):
  try:
    items = session.query(Item).filter_by(category_name = category_name).all()
    return items 
  except:
    return [] 

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
  # Only disconnect a connected user.
  access_token = login_session.get('access_token')
  if access_token is None:
    response = make_response(
    json.dumps('Current user not connected.'), 401)
    flash("You weren't loggen in.") 
  else: 
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
      response = make_response(json.dumps('Successfully disconnected.'), 200)
    else:
      response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    flash("You have successfully been logged out.")

  response.headers['Content-Type'] = 'application/json'
  login_session.pop('access_token', None)
  login_session.pop('picture', None)
  login_session.pop('gplus_id', None)
  login_session.pop('username', None)
  login_session.pop('email', None)
  login_session.pop('picture', None)
  login_session.pop('user_id', None)
  login_session.pop('provider', None)
  return redirect(url_for('showCatalog'))


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'username' in login_session:
      return f(*args, **kwargs)
    else:
      flash("Please login first before proceeding with the action.")
      return redirect('/login')
  return decorated_function

@app.route('/catalog/JSON')
def catalogJSON():
  categories = session.query(Category).all()
  return jsonify(categories = [cat.do_serialize(getItems(cat.name)) for cat in categories])

@app.route('/catalog/<item_title>/JSON')
def itemJSON(item_title):
  item = session.query(Item).filter_by(title=item_title).one_or_none()
  if item:
    return jsonify(item.serialize)
  else:
    return ""


# Show all categories 
@app.route('/')
@app.route('/catalog')
def showCatalog():
  categories = session.query(Category).order_by(asc(Category.name))
  items = session.query(Item).order_by(asc(Item.date_added))
  if 'username' not in login_session:
    return render_template('public_catalog.html', categories = categories, items = items)
  else:
    return render_template('catalog.html', categories = categories, items = items)

# Show category 
@app.route('/catalog/<category_name>/items/')
def showCategory(category_name):
  category = session.query(Category).filter_by(name=category_name).one_or_none()
  if not category:
    flash('The category: %s does not exist' % category_name)
    return showCatalog()

  items = session.query(Item).filter_by(category_name=category_name).all()
  if 'username' not in login_session:
    return render_template('public_category.html', items=items, category=category)
  else:
    return render_template('category.html', items=items, category=category)

# Show item 
@app.route('/catalog/<category_name>/<item_title>/')
def showItem(category_name, item_title):
  category = session.query(Category).filter_by(name=category_name).one_or_none()
  item = session.query(Item).filter_by(title=item_title).one_or_none()
  if not category or not item:
    flash('The item: %s does not exist' % item_title)
    return showCategory(category_name)

  if 'username' not in login_session:
    return render_template('public_item.html', item=item)
  else:
    return render_template('item.html', category = category, item = item)


# Create a new item
@app.route('/catalog/new/', methods=['GET', 'POST'])
@login_required
def newItem():
  if request.method == 'POST':
    category_name = request.form['category_name'].strip()
    if not category_name:
      return "<script>function myFunction() {alert('You must specify category name');}</script><body onload='myFunction()'>"
    
    item_title = request.form['title'].strip()
    if not item_title:
      return "<script>function myFunction() {alert('You must specify item name');}</script><body onload='myFunction()'>"
    
    category = getCategory(category_name)
    if category == None:
      newCategory = Category(name = category_name)
      session.add(newCategory)
      session.commit()

    newItem = Item(title=item_title, description=request.form['description'], 
        category_name=category_name, user_id=login_session['user_id'], date_added = datetime.now())
    session.add(newItem)
    session.commit()
    flash('New %s Item Successfully Created' % (newItem.title))
    return redirect(url_for('showCatalog'))
  else:
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('newitem.html', categories = categories)


# Edit an item
@app.route('/catalog/<category_name>/<item_title>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_name, item_title):
  category = session.query(Category).filter_by(name=category_name).one_or_none()
  itemToEdit = session.query(Item).filter_by(title=item_title).one_or_none()
  if not category or not itemToEdit:
    flash('The item: %s does not exist' % item_title)
    return showCategory(category_name)

  if login_session['user_id'] != itemToEdit.user_id:
      return "<script>function myFunction() {alert('You are not authorized to edit this item');}</script><body onload='myFunction()'>"
  if request.method == 'POST':
    if request.form['title'] and request.form['title'].strip():
      itemToEdit.title = request.form['title'].strip()
    if request.form['description']:
      itemToEdit.description = request.form['description']
    if request.form['category_name'] and request.form['category_name'].strip():
      category_name = request.form['category_name'].strip()
      category = getCategory(category_name)
      if category == None:
        newCategory = Category(name = category_name)
        session.add(newCategory)
        session.commit()
      itemToEdit.category_name = category_name
    itemToEdit.user_id=login_session['user_id']
    session.add(itemToEdit)
    session.commit()
    flash('Item Successfully Edited')
    return redirect(url_for('showItem', category_name = category_name, item_title = itemToEdit.title)) 
  else:
    category = getCategory(category_name)
    categories = session.query(Category).order_by(asc(Category.name))
    return render_template('edititem.html', category=category, item=itemToEdit, categories = categories)

# Delete an item
@app.route('/catalog/<category_name>/<item_title>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_name, item_title):
  category = session.query(Category).filter_by(name=category_name).one_or_none()
  itemToDelete = session.query(Item).filter_by(title=item_title).one_or_none()
  if not category or not itemToDelete:
    flash('The item: %s does not exist' % item_title)
    return showCategory(category_name)

  if login_session['user_id'] != itemToDelete.user_id:
      return "<script>function myFunction() {alert('You are not authorized to delete this item');}</script><body onload='myFunction()'>"
  if request.method == 'POST':
    session.delete(itemToDelete)
    session.commit()
    flash('The Item Successfully Deleted')
    return redirect(url_for('showCategory', category_name = category_name))
  else:
    return render_template('deleteitem.html', category = category, item = itemToDelete)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=8000)
