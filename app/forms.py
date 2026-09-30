from datetime import date

from flask_wtf import FlaskForm

from wtforms import (
    DecimalField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
    ValidationError
)

from app.models import User


class RegistrationForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )


    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=128)
        ]
    )


    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )


    submit = SubmitField(
        "Create Account"
    )


    def validate_username(self, username):

        existing = User.query.filter_by(
            username=username.data.strip()
        ).first()

        if existing:

            raise ValidationError(
                "That username is already taken."
            )


    def validate_email(self, email):

        existing = User.query.filter_by(
            email=email.data.strip().lower()
        ).first()

        if existing:

            raise ValidationError(
                "An account with this email already exists."
            )


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )


    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField(
        "Login"
    )


class TransactionForm(FlaskForm):

    transaction_type = SelectField(
        "Type",

        choices=[
            ("income", "Income"),
            ("expense", "Expense")
        ],

        validators=[
            DataRequired()
        ]
    )


    category = StringField(
        "Category",

        validators=[
            DataRequired(),
            Length(min=2, max=50)
        ]
    )


    amount = DecimalField(
        "Amount",

        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                max=9999999999.99
            )
        ],

        places=2
    )


    description = StringField(
        "Description",

        validators=[
            Optional(),
            Length(max=255)
        ]
    )


    transaction_date = StringField(
        "Date",

        validators=[
            DataRequired()
        ]
    )


    submit = SubmitField(
        "Save Transaction"
    )


    def validate_transaction_date(self, field):

        try:

            parsed = date.fromisoformat(
                field.data
            )

        except (TypeError, ValueError):

            raise ValidationError(
                "Enter a valid date."
            )

        field.data = parsed.isoformat()


class FilterForm(FlaskForm):

    search = StringField(
        "Search",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )


    transaction_type = SelectField(
        "Type",

        choices=[
            ("", "All Types"),
            ("income", "Income"),
            ("expense", "Expense")
        ],

        validators=[
            Optional()
        ]
    )


    category = StringField(
        "Category",

        validators=[
            Optional(),
            Length(max=50)
        ]
    )


    start_date = StringField(
        "From",
        validators=[
            Optional()
        ]
    )


    end_date = StringField(
        "To",
        validators=[
            Optional()
        ]
    )


    submit = SubmitField(
        "Filter"
    )