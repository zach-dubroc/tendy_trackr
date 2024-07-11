# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL to connect to the MySQL database hosted locally in XAMPP
# No password is set; the default MySQL port (3306) is used implicitly
DATABASE_URL = "mysql://root@localhost/trackr_test"

# Creating a new SQLAlchemy engine instance
# This engine communicates with the MySQL database specified by DATABASE_URL
engine = create_engine(DATABASE_URL)

# Creating a configured "Session" class
# autocommit=False means each transaction must be committed explicitly
# autoflush=False means changes are not flushed to the database automatically
# bind=engine tells the sessionmaker to use the engine created above
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Context manager to open and close database sessions
class DatabaseSession:
    def __enter__(self):
        self.db = SessionLocal()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

# Function to get a database session without a generator
def get_db():
    return DatabaseSession()
