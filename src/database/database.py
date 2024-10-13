from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from src.utils.log import Log

# Load environment variables from .env
load_dotenv()

try:
    # Load database connection details from the environment
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    # Conditionally include the password in the connection string
    if DB_PASSWORD:
        DB_PASSWORD = quote_plus(DB_PASSWORD)
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        DATABASE_URL = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    print(f"Database URL: {DATABASE_URL}")

    # Create the SQLAlchemy engine and session
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    Log.INFO("Database engine and session created successfully.")

except Exception as e:
    Log.ERROR(f"Error creating the database engine: {str(e)}")


# Dependency to get DB session
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        Log.ERROR(f"Error during DB session: {str(e)}")
        raise  # Re-raise the exception after logging
    finally:
        if db:
            db.close()
