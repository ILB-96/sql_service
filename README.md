# SQL Database Service

This repository contains a Python-based service that provides a simple and extensible interface for interacting with SQL databases using SQLAlchemy. The service supports basic CRUD (Create, Read, Update, Delete) operations and includes utilities for table validation and execution of SQL queries.

## Features

- **Create and Manage Database Tables**: Automatically create and manage database tables using SQLAlchemy's declarative base.
- **CRUD Operations**: Easily perform CRUD operations (`find_one`, `save_one`, `update_one`, `delete_one`, `find_all`) on database entries.
- **Validation and Execution**: Includes validation of tables and execution of SQL queries with error handling.
- **Session Management**: Manages database sessions for efficient query execution.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/sql-database-service.git
    cd sql-database-service
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Initialization

First, initialize the `SQLDatabase` class with your connection URL:

```python
from sql_database_service import SQLDatabase

# Example: Using an SQLite database
db = SQLDatabase("sqlite:///test.db")
db.create_tables()  # Ensure all tables are created
