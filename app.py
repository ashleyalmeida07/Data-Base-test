from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection details (hardcoded)
DB_HOST = "ep-orange-glitter-a8g7veha.eastus2.azure.neon.tech"
DB_PORT = "5432"
DB_USER = "neondb_owner"
DB_PASSWORD = "esCRTncx1y2t"
DB_NAME = "neondb"

# Create a database connection
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
    )

# API endpoint to handle form submissions
@app.route("/api/contact", methods=["POST"])
def save_contact():
    data = request.json

    # Extract form data
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    phone = data.get("phone")
    email = data.get("email")
    message = data.get("message")

    # Validate required fields
    if not all([first_name, last_name, phone, email, message]):
        return jsonify({"error": "All fields are required"}), 400

    # Save to database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO contacts (first_name, last_name, phone, email, message)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """
        cursor.execute(query, (first_name, last_name, phone, email, message))
        contact_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "contact_id": contact_id}), 201

    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "Database error"}), 500


# Run the server
if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
