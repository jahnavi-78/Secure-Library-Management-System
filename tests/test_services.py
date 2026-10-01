import pytest
from library.services import LibraryService
from library.storage import Storage
from library.models import Book

class MockStorage(Storage):
    def __init__(self):
        self.users = {}
        self.books = {1: Book(1, "Test Book", "Author", True)}
    def _ensure_file_exists(self): pass
    def load_all(self): return self.users, self.books
    def save_all(self, users, books):
        self.users = users
        self.books = books

@pytest.fixture
def service():
    return LibraryService(storage=MockStorage())

def test_register_and_auth(service):
    service.register("user1", "pass123")
    assert service.authenticate("user1", "pass123") is True
    assert service.authenticate("user1", "wrong") is False

def test_borrow_and_return(service):
    service.register("user1", "pass123")
    service.authenticate("user1", "pass123")

    service.borrow_book(1)
    assert service.books[1].available is False
    assert 1 in service.users["user1"].borrowed_books

    service.return_book(1)
    assert service.books[1].available is True
    assert 1 not in service.users["user1"].borrowed_books
