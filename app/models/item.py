from app import db
from flask import jsonify
import json


class Item(db.Model):
    """ORM object for Item table to store item data. Accepts unicode for form
    validation.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
                         db.Unicode(64),
                         index=True,
                         unique=True,
                         nullable=False)
    description = db.Column(
                      db.Unicode(250),
                      index=True,
                      nullable=False)
    picture = db.Column(
                        db.Unicode(250),
                        index=True,)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def serialize(self):
        #JSON serializer property
       return {
           'name'         : self.name,
           'description'  : self.description,
           'picture'      : self.picture,
           'category_id'  : self.category,
           'creator_id'      : self.user_id
       }

    def __repr__(self):
        return '<Item {}>'.format(self.name)
