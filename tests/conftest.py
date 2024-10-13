import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
import psycopg2
import os
from psycopg2 import sql

# Load environment variables for database credentials
DB_USER = os.getenv("DB_USER", "your_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Original and test database names
ORIGINAL_DB_NAME = "nike_campaign_data"
TEST_DB_NAME = "nike_campaign_data_test"

# Full database URLs
ORIGINAL_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ORIGINAL_DB_NAME}"
TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

# SQLAlchemy setup
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    """
    Create the test database by cloning a subset of data from the original database.
    """
    try:
        # Connect to PostgreSQL server (without specifying a database)
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the test database already exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'")
        exists = cursor.fetchone()

        if not exists:
            # Create the test database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(TEST_DB_NAME)))
            print(f"Test database '{TEST_DB_NAME}' created successfully.")

            # Connect to the test database to copy data
            test_conn = psycopg2.connect(
                dbname=TEST_DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            test_cursor = test_conn.cursor()

            # Copy a subset of data from the original database into the test database
            tables = ["campaign", "ad_group", "ad_group_stats"]
            for table in tables:
                test_cursor.execute(sql.SQL(
                    "INSERT INTO {} SELECT * FROM {} LIMIT 100"
                ).format(
                    sql.Identifier(table),
                    sql.Identifier(ORIGINAL_DB_NAME, table)
                ))
                print(f"Copied 100 rows from '{ORIGINAL_DB_NAME}.{table}' to '{TEST_DB_NAME}.{table}'.")

            test_conn.commit()
            test_cursor.close()
            test_conn.close()
            print(f"Data copied to '{TEST_DB_NAME}' successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred while setting up the test database: {e}")


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    """
    Set up the test database before running tests and tear down afterward.
    """
    create_test_database()  # Create the database if it doesn't exist
    # Create tables in the test database
    Base.metadata.create_all(bind=engine)

    yield  # Run tests

    # Drop the tables or the database after tests
    Base.metadata.drop_all(bind=engine)
    drop_test_database()


def drop_test_database():
    """
    Drop the test database to clean up after tests.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(TEST_DB_NAME)))
        cursor.close()
        conn.close()
        print(f"Test database '{TEST_DB_NAME}' dropped successfully.")
    except Exception as e:
        print(f"An error occurred while dropping the test database: {e}")


@pytest.fixture(scope="function")
def db_session():
    """
    Provides a new SQLAlchemy session for each test function.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides a FastAPI TestClient with a database session override.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides[get_db] = get_db
