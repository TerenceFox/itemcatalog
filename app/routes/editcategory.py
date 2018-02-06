from app import app, db
from flask import flash, redirect, url_for, session
from app.forms import editCategoryForm
from app.models.category import Category
from app.models.user import User


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
