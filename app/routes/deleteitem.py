from app import app, db
from flask import redirect, url_for, request, session
from app.forms import deleteItemForm
from app.models.user import User
from app.models.item import Item

@app.route('/deleteitem/', methods=['POST'])
def deleteItem():
    # Associated category specified by query parameter.
    category_id = request.args.get('id')
    # Look for CSRF token in form, verify POST method, and validate form data.
    deleteitem = deleteItemForm()
    if deleteitem.validate_on_submit():
        item = Item.query.filter_by(id=deleteitem.deleteID.data).one()
        if session['user_id'] == item.user_id:
            db.session.delete(item)
            db.session.commit()
            print "Item {} Deleted".format(item.name)
            return redirect(url_for('showCategory', id=category_id))
        else:
            return redirect(url_for('showCategory', id=category_id))
    else:
        return redirect(url_for('showCategory', id=category_id))
