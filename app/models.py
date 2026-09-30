from datetime import datetime
from decimal import Decimal

from flask_login import UserMixin
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app import db, login_manager


class User(UserMixin, db.Model):

    __tablename__ = "users"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
        index=True
    )


    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )


    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    transactions = db.relationship(
        "Transaction",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )


    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )


class Transaction(db.Model):

    __tablename__ = "transactions"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    transaction_type = db.Column(
        db.String(10),
        nullable=False,
        index=True
    )


    category = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )


    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )


    description = db.Column(
        db.String(255),
        nullable=True
    )


    transaction_date = db.Column(
        db.Date,
        nullable=False,
        index=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    user = db.relationship(
        "User",
        back_populates="transactions"
    )


    @property
    def signed_amount(self):

        amount = Decimal(self.amount)

        if self.transaction_type == "income":
            return amount

        return -amount


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )