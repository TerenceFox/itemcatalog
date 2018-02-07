from app import app, db
from flask import redirect, url_for, session
from app.forms import deleteCategoryForm
from app.models.item import Item
from app.models.category import Category
import random
import string
import json
import httplib2
import requests
from oauth2client import client


@app.route('/deletecategory', methods=['POST'])
def deleteCategory():
    """Takes the id of the category associated with the delete button and
    deletes it from the database. Also deletes the items associated with the
    category.
    """
    deletecategory = deleteCategoryForm()
    # Look for CSRF token in form, verify POST method, and validate form data.
    if deletecategory.validate_on_submit():
        deleteID = deletecategory.deleteID.data
        category = Category.query.filter_by(id=deleteID).one()
        # Check logged in user against the category creator.
        if session['user_id'] == category.user_id:
            items = Item.query.filter_by(category=category.id)
            # Delete items related to category as well as category itself.
            if items:
                for i in items:
                    db.session.delete(i)
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
