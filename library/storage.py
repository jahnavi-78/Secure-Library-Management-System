import json
import os
from .models import User, Book

class Storage:
    def __init__(self, filepath='data/library_db.json'):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            initial_data = {
                "users": {},
                "books": [
                    {"book_id": 1, "title": "Clean Code", "author": "Robert C. Martin", "available": True},
                    {"book_id": 2, "title": "Design Patterns", "author": "GoF", "available": True},
                    {"book_id": 3, "title": "Python Crash Course", "author": "Eric Matthes", "available": True}
                ]
            }
            with open(self.filepath, 'w') as f:
                json.dump(initial_data, f, indent=4)

    def load_all(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        users = {k: User(**v) for k, v in data.get('users', {}).items()}
        books = {b['book_id']: Book(**b) for b in data.get('books', [])}
        return users, books

    def save_all(self, users, books):
        data = {
            "users": {k: v.to_dict() for k, v in users.items()},
            "books": [b.to_dict() for b in books.values()]
        }
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)
