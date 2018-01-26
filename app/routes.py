from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import newCategoryForm, editCategoryForm, deleteCategoryForm
from models import Category, User, Item


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    user = User.query.get(1) #TODO: This needs to inherit from the login session
    users = User.query.all()
    categories = Category.query.all()
    newcategory = newCategoryForm()
    editcategory = editCategoryForm()
    deletecategory = deleteCategoryForm()
    return render_template('index_loggedin.html',
                            categories=categories,
                            users=users,
                            newcategory=newcategory,
                            editcategory=editcategory,
                            deletecategory=deletecategory,
                            user=user)


@app.route('/createcategory', methods=['POST'])
def createNewCategory():
    user = User.query.get(1) #TODO: This needs to inherit from the login session
    newcategory = newCategoryForm()
    if request.method == 'POST':
        if newcategory.validate_on_submit():
            category = Category(
            name=newcategory.name.data,
            description=newcategory.description.data,
            user_id=user.id
            )
            db.session.add(category)
            db.session.commit()
            print "Successfully added Category"
            print "User: {}".format(user.id)
            print "Name: {}".format(newcategory.name.data)
            print "Description: {}".format(newcategory.description.data)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))


@app.route('/editcategory', methods=['POST'])
def editCategory():
    user = User.query.get(1) #TODO: This needs to inherit from the login session
    editcategory = editCategoryForm()
    if request.method == 'POST':
        if editcategory.validate_on_submit():
            category = Category.query.filter_by(id=editcategory.id.data).one()
            category.name = editcategory.name.data
            category.description = editcategory.description.data
            db.session.add(category)
            db.session.commit()
            print "Edit Category"
            print "User: {}".format(category.id)
            print "Name: {}".format(category.name)
            print "Description: {}".format(category.description)
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/deletecategory', methods=['POST'])
def deleteCategory():
    user = User.query.get(1) #TODO: This needs to inherit from the login session
    deletecategory = deleteCategoryForm()
    if request.method == 'POST':
        if deletecategory.validate_on_submit():
            category = Category.query.filter_by(id=deletecategory.id.data).one()
            db.session.delete(category)
            db.session.commit()
            print "Delete Category"
            print "User: {}".format(category.id)
            print "Name: {}".format(category.name)
            print "Description: {}".format(category.description)
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))





@app.route('/category/<string:id>')
def showCategory(id):
    category = Category.query.filter_by(id=id).one()
    items = Item.query.filter_by(category=id).all()
    return render_template('category_loggedin.html',
                            category=category,
                            items=items,
                            id=id)
