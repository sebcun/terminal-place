# Imports
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "YourSecretKey")

# Database
DATABASE = os.getenv("DATABASE_URL", "database.db")


# Function: get_db(), returns connections for database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Function: init_db(), creates any table needed
def init_db():
    conn = get_db()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS pixels (
            x INTEGER,
            y INTEGER,
            color TEXT,
            PRIMARY KEY (x, y)
        )"""
    )
    conn.close()


# Run the Flask web server
if __name__ == "__main__":

    # First setup the database to make sure the table exists
    init_db()

    # Run the app
    app.run(debug=True)
