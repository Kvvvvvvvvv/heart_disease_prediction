from flask import Flask, render_template, session
from backend.auth import auth_bp
from backend.user import user_bp
from backend.doctor import doctor_bp
from backend.admin import admin_bp
from backend.chat import chat_bp
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your-secret-key-change-this-in-production'

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(doctor_bp, url_prefix='/api/doctor')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(chat_bp, url_prefix='/api/chat')

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
        from werkzeug.security import generate_password_hash
        
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
        
        # Create doctor profile
        cursor.execute("INSERT INTO doctors (user_id, specialization) VALUES ((SELECT id FROM users WHERE username = 'doctor1'), 'Cardiology')")
        
        # Assign user to doctor
        cursor.execute("INSERT INTO assignments (user_id, doctor_id) VALUES ((SELECT id FROM users WHERE username = 'user1'), (SELECT id FROM users WHERE username = 'doctor1'))")
    
    conn.commit()
    conn.close()

# Routes for serving HTML templates
@app.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        if role == 'admin':
            return render_template('admin.html')
        elif role == 'doctor':
            return render_template('doctor.html')
        else:  # user
            return render_template('user.html')
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/user')
def user_dashboard():
    if 'user_id' in session and session.get('role') in ['user', 'admin', 'doctor']:
        return render_template('user.html')
    return render_template('login.html')

@app.route('/doctor')
def doctor_dashboard():
    if 'user_id' in session and session.get('role') in ['doctor', 'admin']:
        return render_template('doctor.html')
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if 'user_id' in session and session.get('role') == 'admin':
        return render_template('admin.html')
    return render_template('login.html')


# Preserve original functionality from app.py
@app.route('/predict', methods=['POST'])
def predict():
    # This is the original prediction route
    # We'll maintain this for backward compatibility
    try:
        import joblib
        import json
        import pandas as pd
        
        # Load the original model
        model = joblib.load("heart_disease_model.pkl")
        with open("feature_names.json", "r") as f:
            feature_names = json.load(f)
        
        # Get data from request
        data = request.json
        
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
        
        return jsonify({
            'prediction': int(prediction),
            'confidence': confidence,
            'probabilities': {
                'no_disease': float(prediction_proba[0]),
                'has_disease': float(prediction_proba[1])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/features')
def get_features():
    # Return feature names for the frontend
    try:
        with open("feature_names.json", "r") as f:
            feature_names = json.load(f)
        return jsonify({'features': feature_names})
    except Exception as e:
        return jsonify({'error': str(e)})


# Import and expose original routes if they exist
try:
    # Try importing from original app.py
    from app import *
except ImportError:
    pass


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)