# Personal Expense & Finance Tracker

A web-based personal finance management application built with **Python, Flask, SQLAlchemy, HTML, CSS, and SQLite**. The application allows users to manage their income and expenses through a simple and user-friendly web interface.

## About the Project

The **Personal Expense & Finance Tracker** is a Flask-based web application designed to help users record and manage their daily financial transactions.

Users can add income and expenses, view their transaction history, update or delete transactions, and monitor their overall financial balance through the web application.

The project was initially developed as a Python command-line application and was later upgraded to a **Flask web application** to practice backend development, database integration, routing, templates, CRUD operations, and web application architecture.

## Features

* User-friendly web interface
* Add income transactions
* Add expense transactions
* View transaction history
* Update transactions
* Delete transactions
* Calculate total income
* Calculate total expenses
* Calculate current balance
* Categorize transactions
* Store transaction data in a database
* Form validation
* Dynamic web pages using Jinja2 templates
* Database operations using SQLAlchemy
* Responsive interface using HTML and CSS
* User authentication *(if implemented)*

## Technologies Used

### Backend

* Python
* Flask
* SQLAlchemy
* Jinja2

### Frontend

* HTML
* CSS


### Database

* SQLite

### Tools

* VS Code
* Git
* GitHub

## Python & Flask Concepts Used

* Python functions
* Conditional statements
* Loops
* Exception handling
* Modules
* Object-oriented programming
* Flask routing
* HTTP requests and responses
* Jinja2 template rendering
* Templates and template inheritance
* Forms and form handling
* CRUD operations
* SQLAlchemy ORM
* Database relationships
* Sessions and authentication *(if implemented)*

## Application Features

### 1. Dashboard

The dashboard provides an overview of the user's financial information, including:

* Total income
* Total expenses
* Current balance
* Recent transactions

### 2. Add Transaction

Users can add a new transaction by providing:

* Transaction type
* Amount
* Category
* Description
* Date

### 3. View Transactions

Users can view all their recorded transactions in a structured table.

Each transaction displays information such as:

* Transaction ID
* Type
* Amount
* Category
* Description
* Date

### 4. Update Transaction

Users can edit an existing transaction when they need to correct or modify financial information.

### 5. Delete Transaction

Users can delete transactions that are no longer required.

### 6. Financial Calculations

The application automatically calculates:

```text
Total Income
Total Expenses
----------------
Current Balance
```

**Balance = Total Income − Total Expenses**

## Project Architecture

The application follows a basic Flask web application architecture:

```text
User
  │
  ▼
Web Browser
  │
  ▼
Flask Application
  │
  ├── Routes
  │
  ├── Business Logic
  │
  ├── SQLAlchemy ORM
  │
  ▼
SQLite Database
  │
  ▼
Transactions
```

## Project Structure

```text
Personal-Expense-Finance-Tracker/
│
├── app.py
│
├── models.py
│
├── database.py
│
├── requirements.txt
│
├── README.md
├── PROJECT_DOCUMENTATION.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── add_transaction.html
│   ├── edit_transaction.html
│   ├── transactions.html
│   ├── login.html
│   └── register.html
│
├── static/
│   ├── css/
│   └── style.css   
│
└── instance/
    └── finance.db
```

> The exact structure may vary depending on how the project is currently organized.

## Database Design

The application uses **SQLite** as the database and **SQLAlchemy** as the ORM.

### Transactions Table

| Column           | Description             |
| ---------------- | ----------------------- |
| id               | Unique transaction ID   |
| transaction_type | Income or Expense       |
| amount           | Transaction amount      |
| category         | Transaction category    |
| description      | Transaction description |
| transaction_date | Date of transaction     |

If authentication is implemented, the application may also contain a users table.

### Users Table

| Column   | Description     |
| -------- | --------------- |
| id       | Unique user ID  |
| username | User's username |
| email    | User's email    |
| password | Hashed password |

## CRUD Operations

The project implements the four major database operations:

| Operation | Description                  |
| --------- | ---------------------------- |
| Create    | Add a new transaction        |
| Read      | View transactions            |
| Update    | Edit an existing transaction |
| Delete    | Remove a transaction         |

These operations are implemented using **Flask + SQLAlchemy**.

## How the Application Works

### Step 1 — User opens the application

The user accesses the Flask application through a web browser.

```text
Browser → Flask Server
```

### Step 2 — Flask handles the request

Flask receives the HTTP request and determines which route should handle it.

For example:

```text
/add
/transactions
/edit/<id>
/delete/<id>
```

### Step 3 — Database operation

The Flask application communicates with the SQLite database through SQLAlchemy.

```text
Flask
  ↓
SQLAlchemy
  ↓
SQLite
```

### Step 4 — Response is displayed

The retrieved data is passed to a Jinja2 template.

```text
Database
   ↓
Flask
   ↓
Jinja2 Template
   ↓
HTML Page
   ↓
Browser
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Personal-Expense-Finance-Tracker.git
```

Move into the project directory:

```bash
cd Personal-Expense-Finance-Tracker
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The Flask development server will start.

Open the application in your browser using the local address displayed by Flask, commonly:

```text
http://127.0.0.1:5000/
```

## Requirements

The main dependencies include:

```text
Flask
Flask-SQLAlchemy
```

Additional dependencies should be added to `requirements.txt` if features such as authentication or Flask-WTF are used.

## Example Workflow

```text
Register/Login
      ↓
Dashboard
      ↓
Add Income / Expense
      ↓
Transaction Saved
      ↓
View Transactions
      ↓
Edit / Delete Transaction
      ↓
Dashboard Updated
```

## Future Improvements

The project can be further improved by adding:

* Google OAuth authentication
* User-specific transactions
* Expense charts and graphs
* Monthly financial reports
* Search and filtering
* Transaction pagination
* Export transactions to CSV
* Password reset functionality
* REST API
* PostgreSQL database
* Deployment using Render/Railway/AWS
* Improved responsive UI
* Budget management
* Monthly spending analysis

## What I Learned

Through this project, I practiced and learned:

* Flask application structure
* Backend development with Python
* URL routing
* HTTP request handling
* Jinja2 templates
* HTML/CSS integration
* SQLAlchemy ORM
* SQLite database integration
* CRUD operations
* Form handling and validation
* Database modeling
* Authentication concepts
* Connecting frontend, backend, and database
* Git and GitHub project management

## Project Documentation

Detailed project documentation is available in:

```text
PROJECT_DOCUMENTATION.md
```

The documentation contains:

* Project objectives
* System architecture
* Application workflow
* Database design
* Flask routes
* Database models
* CRUD implementation
* Technologies used
* Future improvements

## Author

**Geetika Vishwakarma**

B.Tech – Electronics and Communication Engineering


---

⭐ If you find this project useful, consider giving the repository a star!
