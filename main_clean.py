"""
TravMechanix Intelligent Search API
Enhanced backend for T2India with ambiguity detection and "Suggest & Select" interface
"""

import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import re
import json
from datetime import datetime

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'travmechanix-intelligent-search-2024'

# Enable CORS for all routes
CORS(app, origins="*")

# Auto-learning database for 0-result queries
ZERO_RESULTS_DB = []
OPERATION_REMINDERS = []
CONTACT_SUBMISSIONS = []

def load_auto_learning_data():
    """Load auto-learning data from files"""
    global ZERO_RESULTS_DB, OPERATION_REMINDERS, CONTACT_SUBMISSIONS
    
    try:
        if os.path.exists('zero_results_db.json'):
            with open('zero_results_db.json', 'r') as f:
                ZERO_RESULTS_DB = json.load(f)
    except:
        ZERO_RESULTS_DB = []
    
    try:
        if os.path.exists('operation_reminders.json'):
            with open('operation_reminders.json', 'r') as f:
                OPERATION_REMINDERS = json.load(f)
    except:
        OPERATION_REMINDERS = []
    
    try:
        if os.path.exists('contact_submissions.json'):
            with open('contact_submissions.json', 'r') as f:
                CONTACT_SUBMISSIONS = json.load(f)
    except:
        CONTACT_SUBMISSIONS = []

def save_auto_learning_data():
    """Save auto-learning data to files"""
    try:
        with open('zero_results_db.json', 'w') as f:
            json.dump(ZERO_RESULTS_DB, f, indent=2)
        
        with open('operation_reminders.json', 'w') as f:
            json.dump(OPERATION_REMINDERS, f, indent=2)
        
        with open('contact_submissions.json', 'w') as f:
            json.dump(CONTACT_SUBMISSIONS, f, indent=2)
    except Exception as e:
        print(f"Error saving auto-learning data: {e}")

@app.route('/api/submit-contact', methods=['POST'])
@app.route('/')
def index():
    return "API is running"
def submit_contact():
    """Submit contact details for zero-result queries"""
    data = request.get_json()
    query = data.get('query', '')
    email = data.get('email', '')
    phone = data.get('phone', '')
    reference_id = data.get('reference_id', '')
    
    if not query or not email:
        return jsonify({
            'success': False,
            'error': 'Query and email are required'
        })
    
    # Store contact submission
    contact_submission = {
        'query': query,
        'email': email,
        'phone': phone,
        'reference_id': reference_id,
        'timestamp': datetime.now().isoformat(),
        'status': 'pending_response',
        'follow_up_date': (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() + (4 * 24 * 60 * 60)) * 1000  # 4 days from now
    }
    
    CONTACT_SUBMISSIONS.append(contact_submission)
    
    # Update the corresponding operation reminder with contact details
    for reminder in OPERATION_REMINDERS:
        if reference_id in reminder.get('id', ''):
            reminder['contact_details'] = {
                'email': email,
                'phone': phone,
                'submission_time': datetime.now().isoformat()
            }
            reminder['priority'] = 'high'  # Upgrade priority when contact is provided
            break
    
    save_auto_learning_data()
    
    return jsonify({
        'success': True,
        'message': 'Contact details submitted successfully',
        'reference_id': reference_id,
        'follow_up_timeline': '4 days maximum'
    })

# Load auto-learning data on startup
load_auto_learning_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

