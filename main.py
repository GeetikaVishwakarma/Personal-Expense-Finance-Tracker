from datetime import date
from database import connect_db, create_table


def add_transaction():
    print("\n--- Add Transaction ---")

    print("1. Income")
    print("2. Expense")

    choice = input("Enter your choice: ")

    if choice == "1":
        transaction_type = "Income"

    elif choice == "2":
        transaction_type = "Expense"

    else:
        print("Invalid choice.")
        return

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    transaction_date = date.today().isoformat()

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO transactions
            (transaction_type, amount, category, description, transaction_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type,
            amount,
            category,
            description,
            transaction_date
        ))

    print("Transaction added successfully!")


def view_transactions():
    print("\n--- All Transactions ---")

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, transaction_type, amount,
                   category, description, transaction_date
            FROM transactions
            ORDER BY id DESC
        """)

        transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found.")
        return

    for transaction in transactions:
        print("\n--------------------------------")
        print("ID:", transaction["id"])
        print("Type:", transaction["transaction_type"])
        print(f"Amount: ₹ {transaction['amount']:.2f}")
        print("Category:", transaction["category"])
        print("Description:", transaction["description"])
        print("Date:", transaction["transaction_date"])


def calculate_balance():
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE transaction_type = ?",
            ("Income",)
        )

        income = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE transaction_type = ?",
            ("Expense",)
        )

        expense = cursor.fetchone()[0] or 0

    balance = income - expense

    print("\n--- Financial Summary ---")
    print(f"Total Income  : ₹ {income:.2f}")
    print(f"Total Expense : ₹ {expense:.2f}")
    print(f"Balance       : ₹ {balance:.2f}")


def update_transaction():
    print("\n--- Update Transaction ---")

    try:
        transaction_id = int(input("Enter transaction ID: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    # Find the existing transaction
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, transaction_type, amount,
                   category, description, transaction_date
            FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        transaction = cursor.fetchone()

    if not transaction:
        print("Transaction not found.")
        return

    # Display current transaction
    print("\nCurrent Transaction:")
    print("--------------------------------")
    print("ID:", transaction["id"])
    print("Type:", transaction["transaction_type"])
    print(f"Amount: ₹ {transaction['amount']:.2f}")
    print("Category:", transaction["category"])
    print("Description:", transaction["description"])
    print("Date:", transaction["transaction_date"])

    print("\nEnter new details:")

    # Transaction type
    print("\n1. Income")
    print("2. Expense")

    choice = input("Enter transaction type: ")

    if choice == "1":
        transaction_type = "Income"

    elif choice == "2":
        transaction_type = "Expense"

    else:
        print("Invalid choice.")
        return

    # Amount
    try:
        amount = float(input("Enter new amount: "))

        if amount <= 0:
            print("Amount must be greater than 0.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    # Other details
    category = input("Enter new category: ").strip()
    description = input("Enter new description: ").strip()

    # Keep today's date for the updated transaction
    transaction_date = date.today().isoformat()

    # Update database
    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE transactions
            SET transaction_type = ?,
                amount = ?,
                category = ?,
                description = ?,
                transaction_date = ?
            WHERE id = ?
        """, (
            transaction_type,
            amount,
            category,
            description,
            transaction_date,
            transaction_id
        ))

    print("Transaction updated successfully!")


def delete_transaction():
    print("\n--- Delete Transaction ---")

    try:
        transaction_id = int(input("Enter transaction ID: "))
    except ValueError:
        print("Please enter a valid ID.")
        return

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, transaction_type, amount,
                   category, description, transaction_date
            FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        row = cursor.fetchone()

        if not row:
            print("Transaction not found.")
            return

        print("\nFound transaction:")
        print("ID:", row["id"])
        print("Type:", row["transaction_type"])
        print(f"Amount: ₹ {row['amount']:.2f}")
        print("Category:", row["category"])
        print("Description:", row["description"])
        print("Date:", row["transaction_date"])

        confirm = input("Confirm delete? (y/N): ").strip().lower()

        if confirm != "y":
            print("Delete cancelled.")
            return

        cursor.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )

        print("Transaction deleted successfully!")


def main():
    create_table()

    while True:
        print("\n================================")
        print("   PERSONAL FINANCE TRACKER")
        print("================================")

        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Financial Summary")
        print("4. Update Transaction")
        print("5. Delete Transaction")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()

        elif choice == "2":
            view_transactions()

        elif choice == "3":
            calculate_balance()

        elif choice == "4":
            update_transaction()

        elif choice == "5":
            delete_transaction()

        elif choice == "6":
            print("Thank you for using Personal Finance Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()