from app import app, db
from flask import flash, redirect, url_for, request, session
from app.forms import editItemForm
from app.models.item import Item
from app.models.user import User


@app.route('/edititem/', methods=['POST'])
def editItem():
    """Handles Edit Item form submissions and updates the item associated with
    the edit button.
    """
    user = User.query.filter_by(id=session['user_id']).one()
    edititem = editItemForm()
    # Associated category specified by query parameter.
    category_id = request.args.get('id')
    # Look for CSRF token in form, verify POST method, and validate form data.
    if edititem.validate_on_submit():
        item = Item.query.filter_by(id=edititem.editID.data).one()
        # Check logged in user against the item's creator.
        """
        """
        if session['user_id'] == item.user_id:
            item.name = edititem.name.data
            item.description = edititem.description.data
            if edititem.picture.data:
                item.picture = edititem.picture.data
        else:
            flash("You need to be the owner of this item to edit it.")
            return redirect(url_for('showCategory', id=category_id))
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('showCategory', id=category_id))
    else:
        # If validation failed, roll back database session and provide error
        # messages to user.
        db.session.rollback()
        for field, error in edititem.errors.items():
            for i in error:
                flash("ERROR: {} - {}".format(field, i))
        return redirect(url_for('showCategory', id=category_id))
