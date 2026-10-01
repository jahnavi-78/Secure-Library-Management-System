import hashlib
from .models import User, Book
from .storage import Storage

class LibraryService:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.users, self.books = self.storage.load_all()
        self.current_user = None

    def _hash_pass(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            raise ValueError("Username already exists.")
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")

        self.users[username] = User(username=username, password_hash=self._hash_pass(password))
        self.storage.save_all(self.users, self.books)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        if user and user.password_hash == self._hash_pass(password):
            self.current_user = user
            return True
        return False

    def get_all_books(self):
        return list(self.books.values())

    def borrow_book(self, book_id: int):
        if not self.current_user:
            raise PermissionError("Not authenticated.")
        book = self.books.get(book_id)
        if not book:
            raise ValueError("Book not found.")
        if not book.available:
            raise ValueError("Book is currently borrowed by someone else.")

        book.available = False
        self.current_user.borrowed_books.append(book_id)
        self.storage.save_all(self.users, self.books)

    def return_book(self, book_id: int):
        if not self.current_user:
            raise PermissionError("Not authenticated.")
        if book_id not in self.current_user.borrowed_books:
            raise ValueError("You have not borrowed this book.")

        book = self.books.get(book_id)
        if book:
            book.available = True

        self.current_user.borrowed_books.remove(book_id)
        self.storage.save_all(self.users, self.books)

    def logout(self):
        self.current_user = None
