from app import db


class Category(db.Model):
    """ORM object for Category table to store category data. Accepts unicode
    for form validation.
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
    items = db.relationship('Item', backref='items', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Category: {}>'.format(self.name)
