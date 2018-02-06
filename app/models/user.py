from app import db


class User(db.Model):
    """ORM object for User table, to keep persistent user info and match
    logins to existing users.  
    """
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
