import os
from flask import Flask, flash, jsonify, redirect, render_template, request, \
                    send_from_directory, session, url_for
from werkzeug import secure_filename
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from setup import Base, Category, Item

# Define globals
IS_LOGGED_IN = False
IMAGES_DIRECTORY = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
    if IS_LOGGED_IN:
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
                            creator = session['username'])
            db_session.add(new_item)
            db_session.commit()
            return redirect(url_for('list_categories'))
    else:
        return redirect(url_for('login'))


# Edit item
@app.route('/catalog/<category_name>/<item_name>/edit',
            methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    if IS_LOGGED_IN:
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


# Process user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    global IS_LOGGED_IN
    if request.method == 'POST':
        session['username'] = request.form['username']
        IS_LOGGED_IN = True
        return redirect(url_for('list_categories'))
    else:
        return render_template('login.html', is_login = IS_LOGGED_IN)


# Log user out
@app.route('/logout')
def logout():
    global IS_LOGGED_IN
    # remove the username from the session if its there
    session.pop('username', None)
    IS_LOGGED_IN = False
    return redirect(url_for('list_categories'))


if __name__ == '__main__':
    app.secret_key = 'cgvSdvbFudzOunQFaklmHA=='  # super_secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
