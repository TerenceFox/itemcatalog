from app import app, db
from flask import flash, redirect, url_for, request, session
from app.forms import editItemForm
from app.models.item import Item
from app.models.user import User


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
