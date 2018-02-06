from app import app, db
from flask import flash, redirect, url_for, session
from app.forms import newCategoryForm
from app.models.category import Category
from app.models.user import User


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
