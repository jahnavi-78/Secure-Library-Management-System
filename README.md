# Secure Library Management System

An interview-ready, object-oriented Python application simulating a library system with secure user authentication and book tracking.

## Architecture
- **Models:** `Book`, `User` data classes.
- **Services:** `LibraryService` handles business logic.
- **Storage:** Repository pattern for JSON data persistence.
- **CLI:** Isolated presentation layer.
- **Tests:** `pytest` suite for reliable operation.

## How to Run
```bash
pip install -r requirements.txt
python run.py
```
Run tests: `pytest tests/`
