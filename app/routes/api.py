from app import app, db
from flask import jsonify, make_response
import json
from app.models.item import Item


@app.route('/item/<int:id>/JSON')
def itemJSON(id):
    """Returns JSON data on an item corresponding to the ID in the URL.
    """
    item = Item.query.get(id)
    if item:
        return jsonify(Item=item.serialize)
    else:
        response = make_response(json.dumps(
                   'No item found for id {}'.format(id)),
                   401)
        response.headers['Content-Type'] = 'application/json'
        return response
