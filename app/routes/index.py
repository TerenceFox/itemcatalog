from app import app, db
from flask import render_template, session
from app.forms import newCategoryForm, editCategoryForm, deleteCategoryForm
from app.models.category import Category
from app.models.item import Item
from app.models.user import User
import random
import string

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
