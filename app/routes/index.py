from app import app, db
from flask import render_template, session
from app.forms import newCategoryForm, editCategoryForm, deleteCategoryForm
from app.models.category import Category
from app.models.item import Item
from app.models.user import User
import random
import string


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """Handles the route for the main page, which displays all stored
    categories and starts the login flow by creating a state token. When
    logged in, categories can be created and edited from this page.
    """
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
    is_logged_in = 'username' in session
    return render_template('index.html',
                           categories=categories,
                           Category=Category,
                           users=users,
                           User=User,
                           items=items,
                           newcategory=newcategory,
                           editcategory=editcategory,
                           deletecategory=deletecategory,
                           STATE=state,
                           is_logged_in=is_logged_in)
