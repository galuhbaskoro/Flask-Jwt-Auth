from datetime import datetime
from extentions import db
from werkzeug.security import generate_password_hash, check_password_hash

class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(36), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"TokenBlocklist(id={self.id}, jti={self.jti})"
    
    def save(self):
        db.session.add(self)
        db.session.commit() 
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255))
    role = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"User(username={self.username}, email={self.email}, password={self.password})"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit() 

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    species = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"Animal(name={self.name}, species={self.species}, age={self.age}, owner={self.owner})"    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()