from flask import Blueprint, request, jsonify, session
import sqlite3
import joblib
import json
import pandas as pd
import numpy as np

user_bp = Blueprint('user', __name__)

# Model and feature names will be loaded when needed
model = None
feature_names = None


def load_model_if_needed():
    global model, feature_names
    if model is None or feature_names is None:
        try:
            import joblib
            # Try loading from parent directory first
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
    return model, feature_names

def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
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
            'status': 'success',
            'message': 'Dashboard data retrieved successfully',
            'data': {
                'user': dict(user) if user else None,
                'predictions': [dict(pred) for pred in predictions],
                'assigned_doctor': dict(doctor) if doctor else None
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@user_bp.route('/predict', methods=['POST'])
def predict():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        # Load model if needed
        current_model, current_feature_names = load_model_if_needed()
        
        if not current_model:
            return jsonify({
                'status': 'error', 
                'message': 'Model not loaded',
                'data': {}
            }), 500
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error', 
                    'message': f'Missing required field: {field}',
                    'data': {}
                }), 400
        
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
        input_data = input_data[current_feature_names]
        
        # Make prediction
        prediction = current_model.predict(input_data)[0]
        prediction_proba = current_model.predict_proba(input_data)[0]
        confidence = float(max(prediction_proba))
        
        # Save prediction to database
        conn = get_db_connection()
        patient_data_str = json.dumps(data)
        conn.execute('INSERT INTO predictions (user_id, patient_data, prediction_result, confidence_score) VALUES (?, ?, ?, ?)',
                     (session['user_id'], patient_data_str, int(prediction), confidence))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Prediction completed successfully',
            'data': {
                'prediction': int(prediction),
                'confidence': confidence,
                'probabilities': {
                    'no_disease': float(prediction_proba[0]),
                    'has_disease': float(prediction_proba[1])
                },
                'risk_level': 'High' if prediction_proba[1] > 0.7 else 'Medium' if prediction_proba[1] > 0.3 else 'Low'
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@user_bp.route('/predictions/history', methods=['GET'])
def get_prediction_history():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        user_id = session['user_id']
        
        conn = get_db_connection()
        predictions = conn.execute('''
            SELECT id, patient_data, prediction_result, confidence_score, created_at
            FROM predictions
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,)).fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Prediction history retrieved successfully',
            'data': [dict(pred) for pred in predictions]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@user_bp.route('/request_consultation', methods=['POST'])
def request_consultation():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        # This endpoint would typically notify the assigned doctor
        # For now, we'll just return a success message
        return jsonify({
            'status': 'success',
            'message': 'Consultation request sent to your assigned doctor',
            'data': {}
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@user_bp.route('/assigned_doctor', methods=['GET'])
def get_assigned_doctor():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
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
            return jsonify({
                'status': 'success',
                'message': 'Doctor retrieved successfully',
                'data': dict(doctor)
            })
        else:
            return jsonify({
                'status': 'error', 
                'message': 'No doctor assigned yet',
                'data': {}
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500