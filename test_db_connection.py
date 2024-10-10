import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def create_connection():
    try:
        # Fetch the connection parameters from environment variables
        connection = psycopg2.connect(
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")   # Default PostgreSQL port is '5432'
        )

        # If connection is successful
        print("Connection to PostgreSQL DB successful")
        return connection

    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None

if __name__ == "__main__":
    connection = create_connection()

    if connection:
        # Close the connection after testing
        connection.close()
        print("Connection closed")
