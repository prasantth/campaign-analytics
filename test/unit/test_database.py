from src.database.db_conn import create_connection

def test_create_connection():
    """
    Test if the create_connection function successfully connects to the PostgreSQL database.
    """
    connection = create_connection()

    # Assert that the connection is not None, meaning it was successful
    assert connection is not None, "Failed to connect to the database"

    # If the connection is successful, close it
    if connection:
        connection.close()
