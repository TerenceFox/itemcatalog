from app import app, db
from flask import flash, redirect, url_for, request, session
from app.forms import newItemForm
from app.models.item import Item
from app.models.user import User


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
