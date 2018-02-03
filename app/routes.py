from app import app, db
from flask import render_template, flash, redirect, url_for, request, session,\
                  jsonify, make_response, session
from app.forms import newCategoryForm, editCategoryForm, deleteCategoryForm, \
                      newItemForm, editItemForm, deleteItemForm
from models import Category, User, Item
import random
import string
import json
import httplib2
import requests
from oauth2client import client

"""This module provides all the routing for the website, see detailed comments
below for specific functionality.
"""
# Global variables for OAuth
CLIENT_SECRET_FILE = 'app/client_secret.json'
CLIENT_ID = json.loads(
    open('app/client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


# API Endpoint to retun JSON data for a given item.
@app.route('/item/<int:id>/JSON')
def itemJSON(id):
    item = Item.query.get(id)
    return jsonify(Item=item.serialize)


# Index page for displaying list of categories and recently created items.
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # OAuth Flow - Create a state token to protect against CSRF
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    # Pass generated state token into Flask session
    session['state'] = state
    # DB interface
    users = User.query.all()
    categories = Category.query.all()
    items = Item.query.all()
    # Pass form objects into template.
    newcategory = newCategoryForm()
    editcategory = editCategoryForm()
    deletecategory = deleteCategoryForm()
    # Display logged-in template if user is present in session.
    if 'username' in session:
        user = User.query.filter_by(id=session['user_id']).one()
        return render_template('index_loggedin.html',
                               categories=categories,
                               Category=Category,
                               users=users,
                               User=User,
                               items=items,
                               newcategory=newcategory,
                               editcategory=editcategory,
                               deletecategory=deletecategory,
                               user=user,
                               STATE=state)
    # Logged-out view.
    else:
        return render_template('index.html',
                               categories=categories,
                               Category=Category,
                               users=users,
                               User=User,
                               items=items,
                               STATE=state)


# Handles Google Sign-in flow server-side
@app.route('/gconnect', methods=['POST'])
def gConnect():
    # Step 1: Validate state token.
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Step 2: Obtain authorization code from Google JSON response
    code = request.data
    # Step 3: Exchange auth code for credentials object.
    credentials = client.credentials_from_clientsecrets_and_code(
                  CLIENT_SECRET_FILE,
                  ['profile', 'email'],
                  code)

    # Step 4: API Call to check that the access token is valid.
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

    # Step 5: match access token to current user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Step 6: match access token to app's client ID.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Step 7: Store access token in session for disconnect
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Step 8: API call for user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Step 9: store user info in session
    session['provider'] = 'google'
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    # Step 10: Determine if user exists in database, otherwise create it.
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id
    return redirect(url_for('index'))


# Helper functions for storing users in database.
def createUser(login_session):
    newUser = User(username=session['username'],
                   email=session['email'],
                   picture=session['picture'],
                   password_hash="notused")
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Google Sign-out flow
@app.route('/gdisconnect')
def gdisconnect():
    # Step 1: Check if user is present in session.
    access_token = session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
                   'Current user not connected.'),
                   401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is {}'.format(access_token)
    print 'User name is: '
    print session['username']
    # Step 2: API call to revoke the access token stored in session.
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(session['access_token'])  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    # Step 3: 200 or 400 status both mean the user should be logged out and
    # deleted from session.
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        response = 'Logged out.'
        flash(response)
        return redirect(url_for('index'))
    elif result['status'] == '400':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        response = 'Logged out.'
        flash(response)
        return redirect(url_for('index'))
    else:
        response = 'Failed to revoke token for given user.'
        flash(response)
        return redirect(url_for('index'))


# This route handles form data for creating new categories.
@app.route('/createcategory', methods=['POST'])
def createNewCategory():
    user = User.query.filter_by(id=session['user_id']).one()
    newcategory = newCategoryForm()
    # Look for CSRF token in form, verify POST method, and validate form data.
    if newcategory.validate_on_submit():
        # Create new database entry with form data.
        category = Category(name=newcategory.name.data,
                            description=newcategory.description.data,
                            user_id=user.id)
        db.session.add(category)
        db.session.commit()
        print "Successfully added category"
        print "User: {}".format(user.id)
        print "Name: {}".format(newcategory.name.data)
        print "Description: {}".format(newcategory.description.data)
        return redirect(url_for('index'))
    else:
        # If validation failed, roll back database session and provide error
        # messages to user.
        db.session.rollback()
        for field, error in newcategory.errors.items():
            for i in error:
                flash("ERROR: {} - {}".format(field, i))
        return redirect(url_for('index'))


# This route handles form data for editing existing categories.
@app.route('/editcategory', methods=['POST'])
def editCategory():
    user = User.query.filter_by(id=session['user_id']).one()
    editcategory = editCategoryForm()
    # Look for CSRF token in form, verify POST method, and validate form data.
    if editcategory.validate_on_submit():
        category = Category.query.filter_by(id=editcategory.editID.data).one()
        category.name = editcategory.name.data
        category.description = editcategory.description.data
        # This loop catches an exception thrown in the case of a value not
        # being unique.
        try:
            db.session.add(category)
            db.session.commit()
        except:
            # Clear out database session and provide error message to user.
            db.session.rollback()
            flash("ERROR: Name and description must be unique.")
            return redirect(url_for('index'))
        print "Successfully edited category"
        print "User: {}".format(category.id)
        print "Name: {}".format(category.name)
        print "Description: {}".format(category.description)
        return redirect(url_for('index'))
    else:
        # If validation failed, roll back database session and provide error
        # messages to user.
        db.session.rollback()
        for field, error in editcategory.errors.items():
            for i in error:
                flash("ERROR: {} - {}".format(field, i))
        return redirect(url_for('index'))


# This route handles a form submission to confirm deletion of a category.
@app.route('/deletecategory', methods=['POST'])
def deleteCategory():
    deletecategory = deleteCategoryForm()
    # Look for CSRF token in form, verify POST method, and validate form data.
    if deletecategory.validate_on_submit():
        category = Category.query.filter_by(id=deletecategory.deleteID.data).one()
        items = Item.query.filter_by(category=category.id)
        print "Delete category"
        print "User: {}".format(category.id)
        print "Name: {}".format(category.name)
        print "Description: {}".format(category.description)
        # Delete items related to category as well as category itself.
        if items:
            for i in items:
                db.session.delete(i)
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


# This route shows the items contained with a given category.
@app.route('/category/<string:id>')
def showCategory(id):
    # DB interface.
    category = Category.query.filter_by(id=id).one()
    items = Item.query.filter_by(category=id).all()
    state = session['state']
    if 'username' in session:
        user = User.query.filter_by(id=session['user_id']).one()
        # Pass form objects into template.
        newitem = newItemForm()
        edititem = editItemForm()
        deleteitem = deleteItemForm()
        # Display logged-in template if user is present in session.
        return render_template('category_loggedin.html',
                               STATE=state,
                               user=user,
                               category=category,
                               Category=Category,
                               items=items,
                               id=id,
                               newitem=newitem,
                               edititem=edititem,
                               deleteitem=deleteitem)
    else:
        return render_template('category.html',
                               STATE=state,
                               category=category,
                               Category=Category,
                               items=items,
                               id=id)


# This route handles form data for creating a new item.
@app.route('/createitem/', methods=['POST'])
def createItem():
    user = User.query.filter_by(id=session['user_id']).one()
    newitem = newItemForm()
    # Associated category specified by query parameter.
    category_id = request.args.get('id')
    # Look for CSRF token in form, verify POST method, and validate form data.
    if newitem.validate_on_submit():
        item = Item(name=newitem.name.data,
                    description=newitem.description.data,
                    picture=newitem.picture.data,
                    category=category_id,
                    user_id=user.id)
        db.session.add(item)
        db.session.commit()
        print "Successfully added item"
        print "User: {}".format(item.user_id)
        print "Category: {}".format(item.category)
        print "Name: {}".format(item.name)
        return redirect(url_for('showCategory', id=category_id))
    else:
        # If validation failed, roll back database session and provide error
        # messages to user.
        db.session.rollback()
        for field, error in newitem.errors.items():
            for i in error:
                flash("ERROR: {} - {}".format(field, i))
        return redirect(url_for('showCategory', id=category_id))


@app.route('/edititem/', methods=['POST'])
def editItem():
    user = User.query.filter_by(id=session['user_id']).one()
    edititem = editItemForm()
    # Associated category specified by query parameter.
    category_id = request.args.get('id')
    # Look for CSRF token in form, verify POST method, and validate form data.
    if edititem.validate_on_submit():
        item = Item.query.filter_by(id=edititem.editID.data).one()
        item.name = edititem.name.data
        item.description = edititem.description.data
        if edititem.picture.data:
            item.picture = edititem.picture.data
        db.session.add(item)
        db.session.commit()
        print "Successfully edited item"
        print "User: {}".format(item.user_id)
        print "Category: {}".format(item.category)
        print "Name: {}".format(item.name)
        return redirect(url_for('showCategory', id=category_id))
    else:
        # If validation failed, roll back database session and provide error
        # messages to user.
        db.session.rollback()
        for field, error in edititem.errors.items():
            for i in error:
                flash("ERROR: {} - {}".format(field, i))
        return redirect(url_for('showCategory', id=category_id))


@app.route('/deleteitem', methods=['POST'])
def deleteItem():
    # Associated category specified by query parameter.
    category_id = request.args.get('id')
    # Look for CSRF token in form, verify POST method, and validate form data.
    deleteitem = deleteItemForm()
    if deleteitem.validate_on_submit():
        item = Item.query.filter_by(id=deleteitem.deleteID.data).one()
        db.session.delete(item)
        db.session.commit()
        print "Item {} Deleted".format(item.name)
        return redirect(url_for('showCategory', id=category_id))
    else:
        return redirect(url_for('showCategory', id=category_id))
