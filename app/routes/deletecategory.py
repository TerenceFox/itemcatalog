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


# This route handles a form submission to confirm deletion of a category.
@app.route('/deletecategory', methods=['POST'])
def deleteCategory():
    deletecategory = deleteCategoryForm()
    # Look for CSRF token in form, verify POST method, and validate form data.
    if deletecategory.validate_on_submit():
        category = Category.query.filter_by(id=deletecategory.deleteID.data).one()
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
