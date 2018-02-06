from app import app, db
from flask import render_template, session
from app.forms import newItemForm, editItemForm, deleteItemForm
from app.models.category import Category
from app.models.item import Item
from app.models.user import User


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
