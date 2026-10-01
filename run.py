import os
from library.storage import Storage
from library.services import LibraryService
from library.cli import LibraryCLI

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'library_db.json')

    storage = Storage(filepath=data_path)
    service = LibraryService(storage=storage)
    cli = LibraryCLI(service=service)

    cli.run()

if __name__ == "__main__":
    main()
