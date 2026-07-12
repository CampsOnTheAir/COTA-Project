"""
COTA Backend API - Flask application for managing amateur radio contacts
and campground suggestions database.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cota_db')
}

def get_db():
    """Get database connection"""
    return mysql.connector.connect(**db_config)

# ==================== CONTACTS ENDPOINTS ====================

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Retrieve all contacts or filter by criteria"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Build query with optional filters
        query = """
            SELECT c.*, o.call_sign, p.park_name, p.location
            FROM contacts c
            JOIN operators o ON c.operator_id = o.operator_id
            JOIN parks p ON c.park_id = p.park_id
            ORDER BY c.contact_datetime DESC
            LIMIT 100
        """
        
        cursor.execute(query)
        contacts = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(contacts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts', methods=['POST'])
def create_contact():
    """Add a new contact to the log"""
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        
        # Get or create operator
        cursor.execute(
            "SELECT operator_id FROM operators WHERE call_sign = %s",
            (data['operator_call_sign'],)
        )
        operator = cursor.fetchone()
        
        if not operator:
            cursor.execute(
                """INSERT INTO operators (call_sign, first_name, last_name)
                   VALUES (%s, %s, %s)""",
                (data['operator_call_sign'], 
                 data.get('operator_name', '').split()[0] if data.get('operator_name') else '',
                 data.get('operator_name', '').split()[-1] if data.get('operator_name') else '')
            )
            operator_id = cursor.lastrowid
        else:
            operator_id = operator[0]
        
        # Insert contact
        cursor.execute(
            """INSERT INTO contacts 
               (operator_id, park_id, campground_id, contact_datetime, 
                remote_call_sign, remote_operator_name, frequency_mhz, mode,
                signal_report_sent, signal_report_received, remote_location, notes)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (operator_id, data['park_id'], None, data['contact_datetime'],
             data['remote_call_sign'], data.get('remote_operator_name', ''),
             data['frequency_mhz'], data['mode'],
             data.get('signal_report_sent', ''), data.get('signal_report_received', ''),
             data.get('remote_location', ''), data.get('notes', ''))
        )
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'message': 'Contact logged successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== PARKS ENDPOINTS ====================

@app.route('/api/parks', methods=['GET'])
def get_parks():
    """Get all parks for dropdown"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT park_id, park_name, location FROM parks ORDER BY park_name")
        parks = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(parks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parks', methods=['POST'])
def create_park():
    """Add a new park"""
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            """INSERT INTO parks 
               (park_name, location, state_province, country, latitude, longitude, park_code)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (data['park_name'], data['location'], data.get('state_province', ''),
             data.get('country', 'USA'), data.get('latitude'), data.get('longitude'),
             data.get('park_code', ''))
        )
        
        park_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'park_id': park_id, 'message': 'Park created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== SUGGESTIONS ENDPOINTS ====================

@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Retrieve campground suggestions"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        status_filter = request.args.get('status', '')
        query = "SELECT * FROM campground_suggestions"
        
        if status_filter:
            query += f" WHERE status = '{status_filter}'"
        
        query += " ORDER BY suggested_at DESC LIMIT 100"
        
        cursor.execute(query)
        suggestions = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(suggestions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestions/<int:suggestion_id>', methods=['GET'])
def get_suggestion(suggestion_id):
    """Get a specific suggestion"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM campground_suggestions WHERE suggestion_id = %s", (suggestion_id,))
        suggestion = cursor.fetchone()
        cursor.close()
        db.close()
        
        if not suggestion:
            return jsonify({'error': 'Suggestion not found'}), 404
        
        return jsonify(suggestion), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestions', methods=['POST'])
def create_suggestion():
    """Submit a new campground suggestion"""
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
            """INSERT INTO campground_suggestions 
               (suggester_name, suggester_email, suggester_call_sign, park_name, location,
                state_province, country, latitude, longitude, description, access_information,
                parking_available, power_available, water_available, cell_coverage,
                radio_club_contact, website_url, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending')""",
            (data.get('suggester_name', ''),
             data.get('suggester_email', ''),
             data.get('suggester_call_sign', ''),
             data.get('park_name', ''),
             data.get('location', ''),
             data.get('state_province', ''),
             data.get('country', 'USA'),
             data.get('latitude'),
             data.get('longitude'),
             data.get('description', ''),
             data.get('access_information', ''),
             data.get('parking_available', False),
             data.get('power_available', False),
             data.get('water_available', False),
             data.get('cell_coverage', ''),
             data.get('radio_club_contact', ''),
             data.get('website_url', ''))
        )
        
        suggestion_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'suggestion_id': suggestion_id, 'message': 'Suggestion submitted'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestions/<int:suggestion_id>', methods=['PATCH'])
def update_suggestion(suggestion_id):
    """Update suggestion status (admin function)"""
    try:
        data = request.json
        db = get_db()
        cursor = db.cursor()
        
        status = data.get('status', 'pending')
        admin_notes = data.get('admin_notes', '')
        reviewed_by = data.get('reviewed_by', 'admin')
        
        # If approving, create the park entry
        created_park_id = None
        if status == 'approved':
            cursor.execute(
                "SELECT * FROM campground_suggestions WHERE suggestion_id = %s",
                (suggestion_id,)
            )
            suggestion = cursor.fetchone()
            
            if suggestion:
                # Create park from suggestion
                cursor.execute(
                    """INSERT INTO parks 
                       (park_name, location, state_province, country, latitude, longitude)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (suggestion[4], suggestion[5], suggestion[6], suggestion[7],
                     suggestion[8], suggestion[9])
                )
                created_park_id = cursor.lastrowid
        
        # Update suggestion
        cursor.execute(
            """UPDATE campground_suggestions 
               SET status = %s, admin_notes = %s, reviewed_by = %s, 
                   reviewed_at = NOW(), created_park_id = %s
               WHERE suggestion_id = %s""",
            (status, admin_notes, reviewed_by, created_park_id, suggestion_id)
        )
        
        db.commit()
        cursor.close()
        db.close()
        
        return jsonify({'message': 'Suggestion updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== STATISTICS ENDPOINTS ====================

@app.route('/api/stats/parks', methods=['GET'])
def get_park_stats():
    """Get statistics for all parks"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """SELECT p.park_id, p.park_name, p.location,
                      COUNT(DISTINCT c.contact_id) as total_contacts,
                      COUNT(DISTINCT c.operator_id) as unique_operators,
                      MAX(c.contact_datetime) as last_contact
               FROM parks p
               LEFT JOIN contacts c ON p.park_id = c.park_id
               GROUP BY p.park_id
               ORDER BY total_contacts DESC"""
        )
        stats = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats/operators', methods=['GET'])
def get_operator_stats():
    """Get statistics for all operators"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """SELECT o.operator_id, o.call_sign, o.first_name, o.last_name,
                      COUNT(c.contact_id) as total_contacts,
                      COUNT(DISTINCT c.park_id) as parks_activated,
                      MAX(c.contact_datetime) as last_contact
               FROM operators o
               LEFT JOIN contacts c ON o.operator_id = c.operator_id
               GROUP BY o.operator_id
               ORDER BY total_contacts DESC"""
        )
        stats = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)