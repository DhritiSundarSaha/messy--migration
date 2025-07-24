# 🧹 Code Refactoring Challenge – *Messy Migration*

Welcome! This project is a refactored version of a legacy user management API. The original codebase was functional but had several structural and design flaws. The refactoring focused on improving maintainability, testability, and scalability while preserving core functionality.

---

## 🔧 Project Highlights

### ✅ Key Improvements

- **Refactored using Application Factory Pattern** – promotes modular design.
- **Separated concerns** across files: routes, DB setup, app initialization, configs.
- **Test suite** added with `pytest` for reliable verification of endpoints.
- **Comprehensive documentation** in `CHANGES.md`.

---

## 📁 File Structure

messy-migration/
│
├── app/ # Main Flask application
│ ├── init.py # Application factory (create_app)
│ ├── routes.py # API route definitions
│ ├── db.py # DB connection and session management
│ └── schema.sql # SQL schema for DB tables
│
├── tests/ # Test suite
│ └── test_api.py # Pytest API tests
│
├── app.py # App entry point
├── init_db.py # DB initialization script
├── config.py # Configuration settings
├── requirements.txt # Python dependencies
├── CHANGES.md # Detailed refactoring documentation
└── README.md # This file


---

## 🚀 Getting Started

### 🧰 Prerequisites

- Python 3.8+
- Git (to clone repository)

---

### ⚙️ Setup Instructions

```bash
# Clone the repository
git clone <your-repo-url>
cd messy-migration

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# Start the Flask app
python app.py

The API will be available at: http://localhost:5000
