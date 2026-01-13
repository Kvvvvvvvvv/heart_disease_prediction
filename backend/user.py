from flask import Blueprint, request, jsonify, session
import sqlite3
import joblib
import json
import pandas as pd
import numpy as np

user_bp = Blueprint('user', __name__)

# Load ML model and feature names
try:
    model = joblib.load("../heart_disease_model.pkl")
    with open("../feature_names.json", "r") as f:
        feature_names = json.load(f)
except FileNotFoundError:
    try:
        # Try loading from root directory
        model = joblib.load("heart_disease_model.pkl")
        with open("feature_names.json", "r") as f:
            feature_names = json.load(f)
    except FileNotFoundError:
        print("Model files not found! Please ensure heart_disease_model.pkl and feature_names.json exist.")
        model = None
        feature_names = []

def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    # Get user info
    user = conn.execute('SELECT id, username, role FROM users WHERE id = ?', (user_id,)).fetchone()
    
    # Get prediction history
    predictions = conn.execute('''
        SELECT id, patient_data, prediction_result, confidence_score, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 10
    ''', (user_id,)).fetchall()
    
    # Get assigned doctor
    doctor = conn.execute('''
        SELECT u.id, u.username, u.email
        FROM users u
        JOIN assignments a ON u.id = a.doctor_id
        WHERE a.user_id = ?
    ''', (user_id,)).fetchone()
    
    conn.close()
    
    return jsonify({
        'user': dict(user) if user else None,
        'predictions': [dict(pred) for pred in predictions],
        'assigned_doctor': dict(doctor) if doctor else None
    })

@user_bp.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
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
            },
            'risk_level': 'High' if prediction_proba[1] > 0.7 else 'Medium' if prediction_proba[1] > 0.3 else 'Low'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/predictions/history', methods=['GET'])
def get_prediction_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    predictions = conn.execute('''
        SELECT id, patient_data, prediction_result, confidence_score, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(pred) for pred in predictions])

@user_bp.route('/request_consultation', methods=['POST'])
def request_consultation():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # This endpoint would typically notify the assigned doctor
    # For now, we'll just return a success message
    return jsonify({
        'success': True,
        'message': 'Consultation request sent to your assigned doctor'
    })

@user_bp.route('/assigned_doctor', methods=['GET'])
def get_assigned_doctor():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    doctor = conn.execute('''
        SELECT u.id, u.username, u.email
        FROM users u
        JOIN assignments a ON u.id = a.doctor_id
        WHERE a.user_id = ?
    ''', (user_id,)).fetchone()
    conn.close()
    
    if doctor:
        return jsonify(dict(doctor))
    else:
        return jsonify({'message': 'No doctor assigned yet'}), 404