#import httplib2
import json
import os
import random
import requests
import string
from flask import Flask, flash, jsonify, make_response, redirect, \
                    render_template, request, send_from_directory, url_for
from flask import session as login_session
from werkzeug import secure_filename
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from setup import Base, Category, Item

# Define globals
IS_LOGGED_IN = False
IMAGES_DIRECTORY = 'images'
CLIENT_ID = '88143cc4d646e722384a'
CLIENT_SECRET = '896cbafa5d0ebed1a62c17502ef806e7a911a319'

app = Flask(__name__)

# Use PostgreSQL database, local connection
engine = create_engine('postgresql:///catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Home page
@app.route('/')
@app.route('/catalog')
def list_categories():
    categories = db_session.query(Category).all()
    last_items = db_session.query(Item).order_by(desc(Item.id)).limit(10)
    return render_template('categories.html', categories = categories,
                            items = last_items, is_login = IS_LOGGED_IN)


# View/add items in category
@app.route('/catalog/<category_name>')
def list_items(category_name):
    categories = db_session.query(Category).all()
    category = db_session.query(Category).filter_by(name = category_name).one()
    items = db_session.query(Item).filter_by(category_id = category.id).all()
    return render_template('items.html', categories = categories,
                            name = category.name, count = len(items),
                            items = items, is_login = IS_LOGGED_IN)


# View/edit item
@app.route('/catalog/<category_name>/<item_name>')
def show_item(category_name, item_name):
    item = db_session.query(Item).filter_by(name = item_name).one()
    return render_template('show.html', item = item, is_login = IS_LOGGED_IN)


# Show item image
@app.route('/images/<filename>')
def show_image(filename):
    return send_from_directory(IMAGES_DIRECTORY, filename)


# Add item
@app.route('/catalog/add', methods=['GET', 'POST'])
def add_item():
    if 'username' in login_session:
#    if IS_LOGGED_IN:
        if request.method == 'GET':
            categories = db_session.query(Category).all()
            return render_template('add.html', categories = categories,
                                    is_login = IS_LOGGED_IN)
        elif request.method == 'POST':
            image = request.files['image']
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(IMAGES_DIRECTORY, filename))
            else:
                filename = ''
            new_item = Item(name = request.form['name'],
                            description = request.form['description'],
                            picture = filename,
                            category_id = request.form['category_id'],
                            creator = login_session['username'])
            db_session.add(new_item)
            db_session.commit()
            return redirect(url_for('list_categories'))
    else:
        return redirect(url_for('login'))


# Edit item
@app.route('/catalog/<category_name>/<item_name>/edit',
            methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    if 'username' in login_session:
#    if IS_LOGGED_IN:
        if request.method == 'GET':
            categories = db_session.query(Category).all()
            category = db_session.query(Category).\
                        filter_by(name = category_name).one()
            item = db_session.query(Item).filter_by(name = item_name).one()
            return render_template('edit.html', categories = categories,
                                    category_id = category.id,
                                    item = item,
                                    is_login = IS_LOGGED_IN)
        elif request.method == 'POST':
            image = request.files['image']
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(IMAGES_DIRECTORY, filename))
            else:
                filename = ''
            item = db_session.query(Item).filter_by(name = item_name).one()
            item.name = request.form['name']
            item.description = request.form['description']
            item.picture = filename
            item.category_id = request.form['category_id']
            db_session.add(item)
            db_session.commit()
            return redirect(url_for('list_categories'))
    else:
        return redirect(url_for('login'))


# Show login page
@app.route('/login')
def login():
    global IS_LOGGED_IN
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', client_id = CLIENT_ID, state = state,
                            is_login = IS_LOGGED_IN)


# Process GitHub login
@app.route('/glogin')
def github_login():
    global IS_LOGGED_IN
    #
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Stub begin
    # Here we will check response & handle possible errors
    state = login_session['state']
    code = request.args.get('code')
    # Get access token
    url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    params = { 'client_id' : CLIENT_ID, 'client_secret' : CLIENT_SECRET,
                'code' : code, 'state' : state }
    result = requests.post(url, data = params, headers = headers)
    data = result.json()
    login_session['access_token'] = data['access_token']
    # Stub end
    # Get user info
    url = 'https://api.github.com/user'
    token_param = 'token %s' % login_session['access_token']
    headers = {'Authorization': token_param, 'Accept': 'application/json'}
    result = requests.get(url, headers = headers)
    data = result.json()
    login_session['username'] = data['login']
    login_session['fullname'] = data['name']
    #
    print login_session
    #
    IS_LOGGED_IN = True
    return redirect(url_for('list_categories'))


# Log user out
@app.route('/logout')
def logout():
    global IS_LOGGED_IN
    # Delete access token
    url = 'https://api.github.com/applications/%s/tokens/%s' % (
            CLIENT_ID, login_session['access_token'])
    result = requests.delete(url, auth=(CLIENT_ID, CLIENT_SECRET))
    # Stub begin
    print result.headers
    print result.text
    # Stub end
    # remove the user data from the session if its there
    login_session.pop('access_token', None)
    login_session.pop('state', None)
    login_session.pop('username', None)
    login_session.pop('fullname', None)
    #
    print login_session
    #
    IS_LOGGED_IN = False
    return redirect(url_for('list_categories'))


if __name__ == '__main__':
    app.secret_key = 'cgvSdvbFudzOunQFaklmHA=='  # super_secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
