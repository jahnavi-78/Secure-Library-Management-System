import json
import os
import getpass
import hashlib

DATA_FILE = 'library_db.json'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "books": []}
    with open(DATA_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"users": {}, "books": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def setup_initial_data(data):
    if not data["books"]:
        data["books"] = [
            {"id": 1, "title": "The Python Handbook", "author": "Alice Coder", "available": True},
            {"id": 2, "title": "Secure Systems Architecture", "author": "Bob Builder", "available": True},
            {"id": 3, "title": "Algorithms 101", "author": "Charlie Data", "available": True}
        ]
        save_data(data)

def login():
    data = load_data()
    setup_initial_data(data)
    
    print("\n--- Secure Library Login ---")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()
    
    if username in data["users"] and data["users"][username]["password"] == hash_password(password):
        print("Login successful!")
        return username, data
    else:
        print("Invalid credentials.")
        return None, data

def register():
    data = load_data()
    print("\n--- Register ---")
    username = input("Choose a username: ").strip()
    if username in data["users"]:
        print("User already exists.")
        return
    password = getpass.getpass("Choose a password: ").strip()
    
    data["users"][username] = {
        "password": hash_password(password),
        "borrowed_books": []
    }
    save_data(data)
    print("Registration successful!")

def view_books(data):
    print("\n--- Available Books ---")
    for book in data["books"]:
        status = "Available" if book["available"] else "Borrowed"
        print(f"[{book['id']}] {book['title']} by {book['author']} - {status}")

def borrow_book(username, data):
    view_books(data)
    try:
        book_id = int(input("\nEnter Book ID to borrow: "))
        for book in data["books"]:
            if book["id"] == book_id:
                if book["available"]:
                    book["available"] = False
                    data["users"][username]["borrowed_books"].append(book_id)
                    save_data(data)
                    print(f"You have successfully borrowed '{book['title']}'.")
                else:
                    print("Sorry, this book is currently borrowed by someone else.")
                return
        print("Book ID not found.")
    except ValueError:
        print("Invalid ID format.")

def return_book(username, data):
    borrowed = data["users"][username]["borrowed_books"]
    if not borrowed:
        print("You haven't borrowed any books.")
        return
        
    print("\n--- Your Borrowed Books ---")
    for b_id in borrowed:
        book = next((b for b in data["books"] if b["id"] == b_id), None)
        if book:
            print(f"[{book['id']}] {book['title']}")
            
    try:
        book_id = int(input("\nEnter Book ID to return: "))
        if book_id in borrowed:
            for book in data["books"]:
                if book["id"] == book_id:
                    book["available"] = True
                    data["users"][username]["borrowed_books"].remove(book_id)
                    save_data(data)
                    print(f"You have successfully returned '{book['title']}'.")
                    return
        else:
            print("You haven't borrowed this book.")
    except ValueError:
        print("Invalid ID format.")

def main():
    while True:
        print("\n=== Secure Library Management System ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            user, data = login()
            if user:
                while True:
                    print(f"\n--- Welcome, {user} ---")
                    print("1. View All Books")
                    print("2. Borrow a Book")
                    print("3. Return a Book")
                    print("4. Logout")
                    sub = input("Select an option: ")
                    if sub == '1': view_books(data)
                    elif sub == '2': borrow_book(user, data)
                    elif sub == '3': return_book(user, data)
                    elif sub == '4': break
        elif choice == '2':
            register()
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
