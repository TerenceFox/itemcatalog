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
                        index=true,
                        unique=True)
    password_hash = db.Column(
                              db.String(128),
                              index=true,
                              unique=True,
                              nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)
