from app import app, db
from flask import jsonify
from app.models.item import Item


# API Endpoint to retun JSON data for a given item.
@app.route('/item/<int:id>/JSON')
def itemJSON(id):
    item = Item.query.get(id)
    return jsonify(Item=item.serialize)
