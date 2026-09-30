from flask import (
    flash,
    redirect,
    render_template,
    url_for
)

from flask_login import (
    current_user,
    login_user,
    logout_user
)

from app import db

from app.auth import auth_bp

from app.forms import (
    LoginForm,
    RegistrationForm
)

from app.models import User


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )


    form = RegistrationForm()


    if form.validate_on_submit():

        user = User(

            username=form.username.data.strip(),

            email=form.email.data.strip().lower()

        )


        user.set_password(
            form.password.data
        )


        db.session.add(user)

        db.session.commit()


        flash(
            "Account created successfully. Please log in.",
            "success"
        )


        return redirect(
            url_for("auth.login")
        )


    return render_template(
        "auth/register.html",
        form=form
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )


    form = LoginForm()


    if form.validate_on_submit():

        email = form.email.data.strip().lower()


        user = User.query.filter_by(
            email=email
        ).first()


        if user and user.check_password(
            form.password.data
        ):

            login_user(user)


            flash(
                "Welcome back!",
                "success"
            )


            return redirect(
                url_for("main.dashboard")
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "auth/login.html",
        form=form
    )


@auth_bp.route("/logout")
def logout():

    logout_user()


    flash(
        "You have been logged out.",
        "success"
    )


    return redirect(
        url_for("auth.login")
    )