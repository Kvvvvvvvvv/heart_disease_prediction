from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import sqlite3
import os
import joblib
import json
import pandas as pd
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Load ML model and feature names
try:
    model = joblib.load("heart_disease_model.pkl")
    with open("feature_names.json", "r") as f:
        feature_names = json.load(f)
except FileNotFoundError:
    print("Model files not found! Please ensure heart_disease_model.pkl and feature_names.json exist.")
    model = None
    feature_names = []

# Initialize database
def init_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL, -- 'user', 'doctor', 'admin'
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            patient_data TEXT,
            prediction_result INTEGER,
            confidence_score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Doctors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            specialization TEXT,
            license_number TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Chats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            receiver_id INTEGER,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'sent', -- 'sent', 'delivered', 'read'
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id)
        )
    ''')
    
    # Assignments table (users to doctors)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_id INTEGER,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (doctor_id) REFERENCES users (id)
        )
    ''')
    
    # Insert default users if table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Create default admin
        admin_hash = generate_password_hash("admin123")
        cursor.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                      ("admin", admin_hash, "admin", "admin@hospital.com"))
        
        # Create default doctor
        doctor_hash = generate_password_hash("doctor123")
        cursor.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                      ("doctor1", doctor_hash, "doctor", "doctor1@hospital.com"))
        
        # Create default user
        user_hash = generate_password_hash("user123")
        cursor.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                      ("user1", user_hash, "user", "user1@hospital.com"))
        
        # Assign user to doctor
        cursor.execute("INSERT INTO assignments (user_id, doctor_id) SELECT u.id, d.user_id FROM users u, doctors d WHERE u.username = 'user1' AND d.user_id = (SELECT id FROM users WHERE username = 'doctor1')")
    
    conn.commit()
    conn.close()

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

# Authentication decorator
def login_required(role=None):
    def wrapper(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            if role and session.get('role') != role:
                return redirect(url_for('unauthorized'))
            
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for(session['role'] + '_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return jsonify({'success': True, 'role': user['role']})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/unauthorized')
def unauthorized():
    return "Unauthorized access", 403

# API Routes
@app.route('/api/user/dashboard')
@login_required('user')
def user_dashboard():
    return render_template('user.html')

@app.route('/api/doctor/dashboard')
@login_required('doctor')
def doctor_dashboard():
    return render_template('doctor.html')

@app.route('/api/admin/dashboard')
@login_required('admin')
def admin_dashboard():
    return render_template('admin.html')

# Prediction API
@app.route('/api/predict', methods=['POST'])
@login_required('user')
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        # Prepare input data
        input_data = pd.DataFrame({
            'age': [data['age']],
            'sex': [data['sex']],
            'cp': [data['cp']],
            'trestbps': [data['trestbps']],
            'chol': [data['chol']],
            'fbs': [data['fbs']],
            'restecg': [data['restecg']],
            'thalach': [data['thalach']],
            'exang': [data['exang']],
            'oldpeak': [data['oldpeak']],
            'slope': [data['slope']],
            'ca': [data['ca']],
            'thal': [data['thal']]
        })
        
        # Ensure correct column order
        input_data = input_data[feature_names]
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        prediction_proba = model.predict_proba(input_data)[0]
        confidence = float(max(prediction_proba))
        
        # Save prediction to database
        conn = get_db_connection()
        patient_data_str = json.dumps(data)
        conn.execute('INSERT INTO predictions (user_id, patient_data, prediction_result, confidence_score) VALUES (?, ?, ?, ?)',
                     (session['user_id'], patient_data_str, int(prediction), confidence))
        conn.commit()
        conn.close()
        
        return jsonify({
            'prediction': int(prediction),
            'confidence': confidence,
            'probabilities': {
                'no_disease': float(prediction_proba[0]),
                'has_disease': float(prediction_proba[1])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Chat API
@app.route('/api/chat/send', methods=['POST'])
@login_required()
def send_message():
    data = request.get_json()
    sender_id = session['user_id']
    receiver_id = data.get('receiver_id')
    message = data.get('message')
    
    if not receiver_id or not message:
        return jsonify({'error': 'Receiver ID and message are required'}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO chats (sender_id, receiver_id, message) VALUES (?, ?, ?)',
                 (sender_id, receiver_id, message))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/chat/messages/<int:receiver_id>')
@login_required()
def get_messages(receiver_id):
    user_id = session['user_id']
    
    conn = get_db_connection()
    messages = conn.execute('''
        SELECT c.*, u.username as sender_name
        FROM chats c
        JOIN users u ON c.sender_id = u.id
        WHERE (c.sender_id = ? AND c.receiver_id = ?) OR (c.sender_id = ? AND c.receiver_id = ?)
        ORDER BY c.timestamp ASC
    ''', (user_id, receiver_id, receiver_id, user_id)).fetchall()
    conn.close()
    
    return jsonify([dict(msg) for msg in messages])

@app.route('/api/chat/users')
@login_required('doctor')
def get_chat_users():
    doctor_id = session['user_id']
    
    conn = get_db_connection()
    users = conn.execute('''
        SELECT u.id, u.username, u.role
        FROM users u
        JOIN assignments a ON u.id = a.user_id
        WHERE a.doctor_id = ?
    ''', (doctor_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

# Admin API
@app.route('/api/admin/users')
@login_required('admin')
def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, role, email, created_at FROM users').fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@app.route('/api/admin/doctors')
@login_required('admin')
def get_all_doctors():
    conn = get_db_connection()
    doctors = conn.execute('''
        SELECT u.id, u.username, u.email, d.specialization, d.license_number
        FROM users u
        LEFT JOIN doctors d ON u.id = d.user_id
        WHERE u.role = 'doctor'
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(doctor) for doctor in doctors])

@app.route('/api/admin/assign', methods=['POST'])
@login_required('admin')
def assign_user_to_doctor():
    data = request.get_json()
    user_id = data.get('user_id')
    doctor_id = data.get('doctor_id')
    
    conn = get_db_connection()
    # Remove any existing assignment
    conn.execute('DELETE FROM assignments WHERE user_id = ?', (user_id,))
    # Create new assignment
    conn.execute('INSERT INTO assignments (user_id, doctor_id) VALUES (?, ?)', (user_id, doctor_id))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)