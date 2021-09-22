from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connect to an SQLite database (open file with SQLite db)
SQLALCHEMY_DB_URL = "sqlite:///./app.db"

# check_same_thread argument only used for SQLite
# to allow more than one thread interacting with the db for the same request
engine = create_engine(SQLALCHEMY_DB_URL, connect_args={
                       "check_same_thread": False})

# each instance of the SessionLocal class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# each database models or classes (ORM models) will inherit from the Base class
Base = declarative_base()
