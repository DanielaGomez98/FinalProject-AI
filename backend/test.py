import backend.crud as crud
from backend.deps import DBConnection
from backend.db import create_db

if __name__ == "__main__":
    create_db()
    with DBConnection() as db:
        print(crud.label.fetch_all(db=db))
