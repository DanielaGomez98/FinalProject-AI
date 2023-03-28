from .session import SessionMaker


class DBConnection:
    def __init__(self):
        self.db = SessionMaker()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


# function that returns the connection to the database, which allows me to execute a transaction in that database.
async def get_db():
    with DBConnection() as db:
        yield db
