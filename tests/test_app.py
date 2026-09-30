import pytest

from app import create_app, db

from app.models import (
    User,
    Transaction
)


class TestConfig:

    TESTING = True

    SECRET_KEY = "test-secret"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


@pytest.fixture()
def app():

    app = create_app(TestConfig)


    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()

        db.drop_all()


@pytest.fixture()
def client(app):

    return app.test_client()


def test_home_redirects_to_login(client):

    response = client.get("/")


    assert response.status_code == 302


    assert "/auth/login" in (
        response.headers["Location"]
    )


def test_user_creation(app):

    with app.app_context():

        user = User(

            username="testuser",

            email="test@example.com"
        )


        user.set_password(
            "password123"
        )


        db.session.add(user)

        db.session.commit()


        saved = User.query.filter_by(
            email="test@example.com"
        ).first()


        assert saved is not None


        assert saved.check_password(
            "password123"
        )


        assert not saved.check_password(
            "wrongpassword"
        )


def test_transaction_balance(app):

    with app.app_context():

        user = User(

            username="balanceuser",

            email="balance@example.com"
        )


        user.set_password(
            "password123"
        )


        db.session.add(user)

        db.session.commit()


        income = Transaction(

            transaction_type="income",

            category="Salary",

            amount=50000,

            transaction_date="2026-09-01",

            user_id=user.id
        )


        expense = Transaction(

            transaction_type="expense",

            category="Food",

            amount=1500,

            transaction_date="2026-09-02",

            user_id=user.id
        )


        db.session.add_all(
            [income, expense]
        )


        db.session.commit()


        assert income.signed_amount == 50000

        assert expense.signed_amount == -1500