from app import app, db
from flask import render_template, flash, redirect, url_for, request, session,\
                  jsonify, make_response, session
from app.forms import newCategoryForm, editCategoryForm, deleteCategoryForm, \
                      newItemForm, editItemForm, deleteItemForm
from models import Category, User, Item
import random, string, json, httplib2, requests
from oauth2client import client


CLIENT_SECRET_FILE = 'app/client_secret.json'
CLIENT_ID = json.loads(
    open('app/client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #Generate state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    #Flow-2 Saved in Flask session object
    session['state'] = state
    users = User.query.all()
    categories = Category.query.all()
    newcategory = newCategoryForm()
    editcategory = editCategoryForm()
    deletecategory = deleteCategoryForm()
    if 'username' in session:
        user = User.query.filter_by(id=session['user_id']).one()
        return render_template('index_loggedin.html',
                                categories=categories,
                                users=users,
                                newcategory=newcategory,
                                editcategory=editcategory,
                                deletecategory=deletecategory,
                                user=user,
                                STATE=state)
    else:
        return render_template('index.html',
                                categories=categories,
                                users=users,
                                STATE=state)



@app.route('/gconnect', methods=['POST'])
def gConnect():
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    #Exchange auth code for credentials
    credentials = client.credentials_from_clientsecrets_and_code(
    CLIENT_SECRET_FILE,
    ['profile', 'email'],
    code)

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print result
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
    #Store access token for disconnect
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id


    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['provider'] = 'google'
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id
    return redirect(url_for('index'))

# User Helper Functions
def createUser(login_session):
    newUser = User(username=session['username'],
                   email=session['email'],
                   picture=session['picture'],
                   password_hash="notused")
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is {}'.format(access_token)
    print 'User name is: '
    print session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token={}'.format(session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        response = 'Successfully disconnected.'
        flash(response)
        return redirect(url_for('index'))
    elif result['status'] == '400':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        response = 'Login session has timed out. Please sign in again.'
        flash(response)
        return redirect(url_for('index'))
    else:
        response = 'Failed to revoke token for given user.'
        flash(response)
        return redirect(url_for('index'))


@app.route('/createcategory', methods=['POST'])
def createNewCategory():
    user = User.query.filter_by(id=session['user_id']).one()
    newcategory = newCategoryForm()
    if request.method == 'POST':
        if newcategory.validate_on_submit():
            category = Category(
            name=newcategory.name.data,
            description=newcategory.description.data,
            user_id=user.id
            )
            db.session.add(category)
            db.session.commit()
            print "Successfully added category"
            print "User: {}".format(user.id)
            print "Name: {}".format(newcategory.name.data)
            print "Description: {}".format(newcategory.description.data)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))


@app.route('/editcategory', methods=['POST'])
def editCategory():
    user = User.query.filter_by(id=session['user_id']).one()
    editcategory = editCategoryForm()
    if request.method == 'POST':
        if editcategory.validate_on_submit():
            category = Category.query.filter_by(id=editcategory.id.data).one()
            category.name = editcategory.name.data
            category.description = editcategory.description.data
            db.session.add(category)
            db.session.commit()
            print "Edit category"
            print "User: {}".format(category.id)
            print "Name: {}".format(category.name)
            print "Description: {}".format(category.description)
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/deletecategory', methods=['POST'])
def deleteCategory():
    user = User.query.filter_by(id=session['user_id']).one()
    deletecategory = deleteCategoryForm()
    if request.method == 'POST':
        if deletecategory.validate_on_submit():
            category = Category.query.filter_by(id=deletecategory.id.data).one()
            items = Item.query.filter_by(category=category.id).all()
            db.session.delete(category)
            for i in items:
                db.session.delete(i)
            db.session.commit()
            print "Delete category"
            print "User: {}".format(category.id)
            print "Name: {}".format(category.name)
            print "Description: {}".format(category.description)
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/category/<string:id>')
def showCategory(id):
    category = Category.query.filter_by(id=id).one()
    items = Item.query.filter_by(category=id).all()
    state = session['state']
    if 'username' in session:
        user = User.query.filter_by(id=session['user_id']).one()
        if user.id == category.user_id:
            newitem = newItemForm()
            edititem = editItemForm()
            deleteitem = deleteItemForm()
            return render_template('category_loggedin.html',
                                   STATE=state,
                                   user=user,
                                   category=category,
                                   items=items,
                                   id=id,
                                   newitem=newitem,
                                   edititem=edititem,
                                   deleteitem=deleteitem)

    else:
        return render_template('category.html',
                               STATE=state,
                               category=category,
                               items=items,
                               id=id)


@app.route('/createitem/', methods=['POST'])
def createItem():
    user = User.query.filter_by(id=session['user_id']).one()
    newitem = newItemForm()
    category_id = request.args.get('id')
    if request.method == 'POST':
        if newitem.validate_on_submit():
            item = Item(
            name=newitem.name.data,
            description=newitem.description.data,
            picture=newitem.picture.data,
            category=category_id,
            user_id=user.id
            )
            db.session.add(item)
            db.session.commit()
            print "Successfully added item"
            print "User: {}".format(item.user_id)
            print "Category: {}".format(item.category)
            print "Name: {}".format(item.name)
            return redirect(url_for('showCategory', id=category_id))
        else:
            return redirect(url_for('showCategory', id=category_id))


@app.route('/edititem/', methods=['POST'])
def editItem():
    user = User.query.filter_by(id=session['user_id']).one()
    edititem = editItemForm()
    category_id = request.args.get('id')
    if request.method == 'POST':
        if edititem.validate_on_submit():
            item = Item.query.filter_by(id=edititem.id.data).one()
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
            return redirect(url_for('showCategory', id=category_id))


@app.route('/deleteitem', methods=['POST'])
def deleteItem():
    user = User.query.filter_by(id=session['user_id']).one()
    edititem = editItemForm()
    category_id = request.args.get('id')
