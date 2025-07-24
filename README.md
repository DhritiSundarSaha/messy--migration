
In accordance with the submission guidelines, I have pushed the complete refactored codebase to a new Git repository. The central documentation for this project is the **`CHANGES.md`** file, which details:
* Major issues identified in the original code.
* A full breakdown of the changes I made and the reasoning behind them.
* The assumptions and trade-offs considered during the process.
* Potential improvements that could be made with additional time.
**Project Architecture**
The project has been refactored to use the Application Factory pattern, which promotes a modular and scalable structure. This separates concerns, making the codebase cleaner and easier to maintain and test.

*The file structure is as follows:*
messy-migration/
│
├── app/                  # Main Flask application package
│   ├── __init__.py       # Contains the application factory (create_app)
│   ├── routes.py         # Defines all API endpoints (views)
│   ├── db.py             # Manages the database connection and session
│   └── schema.sql        # The SQL schema for creating the database tables
│
├── tests/                # Contains all application tests
│   └── test_api.py       # Pytest suite for the API
│
├── app.py                # The entry point to start the application
├── init_db.py            # Script to initialize the development database
├── config.py             # Application configuration settings
├── requirements.txt      # Project dependencies
├── CHANGES.md            # Detailed log of all refactoring changes
└── README.md             # This file

# Code Refactoring Challenge

## Overview
You've inherited a legacy user management API that works but has significant issues. Your task is to refactor and improve this codebase while maintaining its functionality.

## Getting Started

### Prerequisites
- Python 3.8+ installed
- 3 hours of uninterrupted time

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd messy-migration

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Start the application
python app.py

# The API will be available at http://localhost:5000
