from sqlalchemy.sql import expression
from sqlalchemy_utils import force_auto_coercion, PasswordType, EmailType, URLType

from links import db, app


# Enables assignment of plaintext to the password field, text to int fields and others. See docs.
force_auto_coercion()


def _get_random_id(length, *models):
    from links.helpers import get_random_string

    def _find():
        for model in models:
            if model.query.get(rnd):
                return True
        return False

    while True:
        rnd = get_random_string(length)
        if not _find():
            return rnd


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, info={'label': 'ID'})
    email = db.Column(EmailType(), index=True, unique=True, info={'label': 'Email'})
    name = db.Column(db.String, index=True, nullable=False, info={'label': 'Name'})
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']), nullable=False, info={'label': 'Password'})
    active = db.Column(db.Boolean, default=False, server_default=expression.false(), info={'label': 'Active'})
    admin = db.Column(db.Boolean, nullable=False, default=False, server_default=expression.false(), info={'label': 'Admin'})

    tokens = db.relationship('Token', backref='owner', lazy='dynamic', passive_deletes=True, passive_updates=True)

    @property
    def is_authenticated(self):
        return self.active

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_token(self, token_id):
        for token in self.tokens:
            if token.id == token_id:
                return token
        return None

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.id


class Token(db.Model):
    id = db.Column(db.String, primary_key=True, info={'label': 'ID'})
    active = db.Column(db.Boolean, default=True, server_default=expression.true(), info={'label': 'Active'})
    identity = db.Column(db.String, index=True, nullable=False, info={'label': 'Identity'})

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    links = db.relationship('Link', backref='token', lazy='dynamic', passive_deletes=True, passive_updates=True)

    def __init__(self, user, identity):
        self.user_id = user.id
        self.identity = identity
        self.generate_id()

    def generate_id(self):
        self.id = _get_random_id(app.config['TOKEN_LENGTH'], Token, RemovedToken)
        return self.id

    def delete(self):
        for link in self.links:
            link.delete()
        db.session.add(RemovedToken(self))
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Token %r %r>' % (self.user_id, self.id)


class RemovedToken(db.Model):
    id = db.Column(db.String, primary_key=True, info={'label': 'ID'})

    def __init__(self, token):
        self.id = token.id

    def __repr__(self):
        return '<RemovedToken %r>' % self.id


class Link(db.Model):
    id = db.Column(db.String, primary_key=True, info={'label': 'ID'})
    active = db.Column(db.Boolean, default=True, server_default=expression.true(), info={'label': 'Active'})
    url = db.Column(URLType(), nullable=False, info={'label': 'URL'})

    token_id = db.Column(db.String, db.ForeignKey('token.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __init__(self, token, url):
        self.token_id = token.id
        self.generate_id()
        self.url = url

    def generate_id(self):
        self.id = _get_random_id(app.config['LINK_LENGTH'], Link, RemovedLink)
        return self.id

    def delete(self):
        db.session.add(RemovedLink(self))
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Link %r %r %r>' % (self.token_id, self.id, self.url)


class RemovedLink(db.Model):
    id = db.Column(db.String, primary_key=True, info={'label': 'ID'})

    def __init__(self, link):
        self.id = link.id

    def __repr__(self):
        return '<RemovedLink %r>' % self.id
