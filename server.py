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

# Board Setups
WIDTH = int(os.getenv("BOARD_WIDTH", 100))
HEIGHT = int(os.getenv("BOARD_HEIGHT", 25))

# Database Functions
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


# API Endpoint /api/pixels RETURNS all pixels in a json format.
@app.route("/api/pixels", methods=["GET"])
def get_pixels():
    # Get data from database
    conn = get_db()
    pixels = conn.execute("SELECT x, y, color FROM pixels").fetchall()
    conn.close()

    # Return success with data
    return jsonify([dict(p) for p in pixels]), 200


# API Endpoint /api/place PLACES a pixel and returns success.
@app.route("/api/place", methods=["POST"])
def place_pixel():
    # Get request data
    data = request.get_json()
    x = data["x"]
    y = data["y"]
    color = data["color"]

    # Validate that all fields are sent to create a pixel
    if not x or not y or not color:
        return jsonify({"error": "All fields required."}), 400

    # Validate the X and Y are valid/within boundaries
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return jsonify({"error": "Pixel coordinates are out of bounds."}), 400

    # Add to database
    conn = get_db()
    conn.execute(
        "INSERT OR REPLACE INTO pixels (x, y, color) VALUES (?, ?, ?)", (x, y, color)
    )
    conn.commit()
    conn.close()

    # Return success
    return jsonify({"status": "ok", "pixel": {"x": x, "y": y, "color": color}}), 201


# Run the Flask web server
if __name__ == "__main__":

    # First setup the database to make sure the table exists
    init_db()

    # Run the app
    app.run(debug=True)
