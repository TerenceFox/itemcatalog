from app import app, db
from flask import flash, redirect, url_for, session
from app.forms import newCategoryForm
from app.models.category import Category
from app.models.user import User


@app.route('/createcategory', methods=['POST'])
def createNewCategory():
    """Handler for form submissions from the New Category form. Creates the
    category in the database, associates it with the current user and
    redirects back to the index page.
    """
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
        return redirect(url_for('index'))
    else:
        # If validation failed, roll back database session and provide error
        # messages to user.
        db.session.rollback()
        for field, error in newcategory.errors.items():
            for i in error:
                flash("ERROR: {} - {}".format(field, i))
        return redirect(url_for('index'))
