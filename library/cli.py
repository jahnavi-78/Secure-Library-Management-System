import getpass
from .services import LibraryService

class LibraryCLI:
    def __init__(self, service: LibraryService):
        self.service = service

    def run(self):
        while True:
            print("\n=== Secure Library Management System ===")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Select an option: ").strip()

            try:
                if choice == '1':
                    self._login()
                elif choice == '2':
                    self._register()
                elif choice == '3':
                    break
                else:
                    print("Invalid option.")
            except Exception as e:
                print(f"System Error: {str(e)}")

    def _register(self):
        print("\n--- Register ---")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        try:
            self.service.register(username, password)
            print("Registration successful!")
        except ValueError as e:
            print(f"Error: {str(e)}")

    def _login(self):
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()
        if self.service.authenticate(username, password):
            print("Login successful!")
            self._user_menu()
        else:
            print("Invalid credentials.")

    def _user_menu(self):
        while True:
            print(f"\n--- Welcome, {self.service.current_user.username} ---")
            print("1. View All Books")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. Logout")
            choice = input("Select an option: ").strip()

            try:
                if choice == '1':
                    books = self.service.get_all_books()
                    for b in books:
                        status = "Available" if b.available else "Borrowed"
                        print(f"[{b.book_id}] {b.title} by {b.author} - {status}")
                elif choice == '2':
                    book_id = int(input("Enter Book ID to borrow: "))
                    self.service.borrow_book(book_id)
                    print("Book borrowed successfully!")
                elif choice == '3':
                    book_id = int(input("Enter Book ID to return: "))
                    self.service.return_book(book_id)
                    print("Book returned successfully!")
                elif choice == '4':
                    self.service.logout()
                    break
                else:
                    print("Invalid option.")
            except ValueError as e:
                print(f"Input Error: {str(e)}")
            except Exception as e:
                print(f"Error: {str(e)}")
