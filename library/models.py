from dataclasses import dataclass, field
from typing import List

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    available: bool = True

    def to_dict(self):
        return {"book_id": self.book_id, "title": self.title, "author": self.author, "available": self.available}

@dataclass
class User:
    username: str
    password_hash: str
    borrowed_books: List[int] = field(default_factory=list)

    def to_dict(self):
        return {"username": self.username, "password_hash": self.password_hash, "borrowed_books": self.borrowed_books}
