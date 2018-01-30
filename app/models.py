from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
                         db.String(64),
                         index=True,
                         unique=True,
                         nullable=False)
    email = db.Column(
                      db.String(120),
                      index=True,
                      unique=True,
                      nullable=False)
    picture = db.Column(
                        db.String(250),
                        index=True,
                        unique=True)
    password_hash = db.Column(
                              db.String(128),
                              index=True,
                              unique=True)
    categories = db.relationship('Category', backref='creator', lazy='dynamic')
    items = db.relationship('Item', backref='creator', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
                         db.Unicode(64),
                         index=True,
                         unique=True,
                         nullable=False)
    description = db.Column(
                      db.Unicode(250),
                      index=True,
                      unique=True,
                      nullable=False)
    items = db.relationship('Item', backref='items', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Category: {}>'.format(self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
                         db.Unicode(64),
                         index=True,
                         unique=True,
                         nullable=False)
    description = db.Column(
                      db.Unicode(250),
                      index=True,
                      unique=True,
                      nullable=False)
    picture = db.Column(
                        db.Unicode(250),
                        index=True,)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)
