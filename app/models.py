from flask_login import UserMixin
from . import db
from uuid import uuid4
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    amount = db.Column(db.Float, nullable = False)
    sender_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    referer_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    referer_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    accounts = db.relationship("Account", back_populates="user")

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255), nullable=False, default=lambda: str(uuid4()))
    balance = db.Column(db.Float, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="accounts")


    def __repr__(self):
        return f"Account ({self.number})"
