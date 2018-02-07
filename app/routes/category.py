from app import app, db
from flask import render_template, session
from app.forms import newItemForm, editItemForm, deleteItemForm
from app.models.category import Category
from app.models.item import Item
from app.models.user import User


@app.route('/category/<string:id>')
def showCategory(id):
    """Handler for the page displayed when a category is selected. Shows all
    items within the category.
    """
    # Pass in the category specified by the URL as an object to the template
    category = Category.query.filter_by(id=id).one()
    # Pass in all associated items to the template as an object.
    items = Item.query.filter_by(category=id).all()
    # Pass in session state token obtained from index.
    state = session['state']
    # Detect whether a user is present in session or not and pass a boolean
    # into the template.
    is_logged_in = 'username' in session
    # Pass form objects into template.
    newitem = newItemForm()
    edititem = editItemForm()
    deleteitem = deleteItemForm()
    return render_template('category.html',
                           STATE=state,
                           category=category,
                           User=User,
                           Category=Category,
                           items=items,
                           id=id,
                           newitem=newitem,
                           edititem=edititem,
                           deleteitem=deleteitem,
                           is_logged_in=is_logged_in)
