import csv
import io

from datetime import date
from decimal import Decimal

from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from sqlalchemy import (
    func,
    or_
)

from app import db

from app.forms import (
    FilterForm,
    TransactionForm
)

from app.main import main_bp

from app.models import Transaction


@main_bp.route("/")
def index():

    if current_user.is_authenticated:

        return redirect(
            url_for("main.dashboard")
        )


    return redirect(
        url_for("auth.login")
    )


@main_bp.route("/dashboard")
@login_required
def dashboard():

    base_query = Transaction.query.filter_by(
        user_id=current_user.id
    )


    total_income = (

        db.session.query(
            func.coalesce(
                func.sum(Transaction.amount),
                0
            )
        )

        .filter_by(
            user_id=current_user.id,
            transaction_type="income"
        )

        .scalar()
    )


    total_expense = (

        db.session.query(
            func.coalesce(
                func.sum(Transaction.amount),
                0
            )
        )

        .filter_by(
            user_id=current_user.id,
            transaction_type="expense"
        )

        .scalar()
    )


    total_income = Decimal(
        total_income
    )

    total_expense = Decimal(
        total_expense
    )


    balance = (
        total_income -
        total_expense
    )


    recent_transactions = (

        base_query

        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.id.desc()
        )

        .limit(8)

        .all()
    )


    category_totals = (

        db.session.query(
            Transaction.category,
            func.sum(
                Transaction.amount
            ).label("total")
        )

        .filter_by(
            user_id=current_user.id,
            transaction_type="expense"
        )

        .group_by(
            Transaction.category
        )

        .order_by(
            func.sum(
                Transaction.amount
            ).desc()
        )

        .limit(5)

        .all()
    )


    return render_template(
        "dashboard.html",

        total_income=total_income,

        total_expense=total_expense,

        balance=balance,

        recent_transactions=recent_transactions,

        category_totals=category_totals
    )


@main_bp.route("/transactions")
@login_required
def transactions():

    form = FilterForm(
        request.args,
        meta={"csrf": True}
    )


    query = Transaction.query.filter_by(
        user_id=current_user.id
    )


    search = request.args.get(
        "search",
        ""
    ).strip()


    transaction_type = request.args.get(
        "transaction_type",
        ""
    ).strip()


    category = request.args.get(
        "category",
        ""
    ).strip()


    start_date = request.args.get(
        "start_date",
        ""
    ).strip()


    end_date = request.args.get(
        "end_date",
        ""
    ).strip()


    if search:

        query = query.filter(

            or_(

                Transaction.description.ilike(
                    f"%{search}%"
                ),

                Transaction.category.ilike(
                    f"%{search}%"
                )
            )
        )


    if transaction_type in {
        "income",
        "expense"
    }:

        query = query.filter(
            Transaction.transaction_type ==
            transaction_type
        )


    if category:

        query = query.filter(
            Transaction.category.ilike(
                f"%{category}%"
            )
        )


    if start_date:

        try:

            query = query.filter(
                Transaction.transaction_date >=
                date.fromisoformat(start_date)
            )

        except ValueError:

            flash(
                "Invalid start date ignored.",
                "warning"
            )


    if end_date:

        try:

            query = query.filter(
                Transaction.transaction_date <=
                date.fromisoformat(end_date)
            )

        except ValueError:

            flash(
                "Invalid end date ignored.",
                "warning"
            )


    transaction_list = (

        query

        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.id.desc()
        )

        .all()
    )


    return render_template(
        "transactions.html",

        transactions=transaction_list,

        form=form
    )


@main_bp.route(
    "/transactions/add",
    methods=["GET", "POST"]
)
@login_required
def add_transaction():

    form = TransactionForm()


    if request.method == "GET":

        form.transaction_date.data = (
            date.today().isoformat()
        )


    if form.validate_on_submit():

        transaction = Transaction(

            transaction_type=
                form.transaction_type.data,

            category=
                form.category.data.strip().title(),

            amount=
                form.amount.data,

            description=
                (form.description.data or "").strip(),

            transaction_date=
                date.fromisoformat(
                    form.transaction_date.data
                ),

            user_id=
                current_user.id
        )


        db.session.add(
            transaction
        )

        db.session.commit()


        flash(
            "Transaction added successfully.",
            "success"
        )


        return redirect(
            url_for("main.transactions")
        )


    return render_template(

        "transaction_form.html",

        form=form,

        title="Add Transaction"
    )


@main_bp.route(
    "/transactions/<int:transaction_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_transaction(
    transaction_id
):

    transaction = Transaction.query.filter_by(

        id=transaction_id,

        user_id=current_user.id

    ).first_or_404()


    form = TransactionForm(
        obj=transaction
    )


    if request.method == "GET":

        form.transaction_date.data = (
            transaction.transaction_date.isoformat()
        )


    if form.validate_on_submit():

        transaction.transaction_type = (
            form.transaction_type.data
        )


        transaction.category = (
            form.category.data
            .strip()
            .title()
        )


        transaction.amount = (
            form.amount.data
        )


        transaction.description = (
            form.description.data or ""
        ).strip()


        transaction.transaction_date = (
            date.fromisoformat(
                form.transaction_date.data
            )
        )


        db.session.commit()


        flash(
            "Transaction updated successfully.",
            "success"
        )


        return redirect(
            url_for("main.transactions")
        )


    return render_template(

        "transaction_form.html",

        form=form,

        title="Edit Transaction"
    )


@main_bp.route(
    "/transactions/<int:transaction_id>/delete",
    methods=["POST"]
)
@login_required
def delete_transaction(
    transaction_id
):

    transaction = Transaction.query.filter_by(

        id=transaction_id,

        user_id=current_user.id

    ).first_or_404()


    db.session.delete(
        transaction
    )

    db.session.commit()


    flash(
        "Transaction deleted successfully.",
        "success"
    )


    return redirect(
        url_for("main.transactions")
    )


@main_bp.route(
    "/transactions/export"
)
@login_required
def export_transactions():

    transactions = (

        Transaction.query

        .filter_by(
            user_id=current_user.id
        )

        .order_by(
            Transaction.transaction_date.desc()
        )

        .all()
    )


    output = io.StringIO()

    writer = csv.writer(
        output
    )


    writer.writerow([
        "ID",
        "Type",
        "Category",
        "Amount",
        "Description",
        "Date"
    ])


    for transaction in transactions:

        writer.writerow([

            transaction.id,

            transaction.transaction_type.title(),

            transaction.category,

            transaction.amount,

            transaction.description or "",

            transaction.transaction_date.isoformat()
        ])


    response = make_response(
        output.getvalue()
    )


    response.headers["Content-Type"] = (
        "text/csv"
    )


    response.headers["Content-Disposition"] = (
        "attachment; "
        "filename=finance_transactions.csv"
    )


    return response