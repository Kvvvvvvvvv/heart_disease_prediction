from flask import Blueprint, request, jsonify, session
import sqlite3

doctor_bp = Blueprint('doctor', __name__)

def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@doctor_bp.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'error': 'Not authorized'}), 401
    
    doctor_id = session['user_id']
    
    conn = get_db_connection()
    # Get doctor info
    doctor = conn.execute('SELECT id, username, email FROM users WHERE id = ?', (doctor_id,)).fetchone()
    
    # Get assigned users
    assigned_users = conn.execute('''
        SELECT u.id, u.username, u.email
        FROM users u
        JOIN assignments a ON u.id = a.user_id
        WHERE a.doctor_id = ?
    ''', (doctor_id,)).fetchall()
    
    # Get recent consultations
    consultations = conn.execute('''
        SELECT p.id, p.user_id, p.prediction_result, p.confidence_score, p.created_at, u.username
        FROM predictions p
        JOIN users u ON p.user_id = u.id
        WHERE p.user_id IN (
            SELECT user_id FROM assignments WHERE doctor_id = ?
        )
        ORDER BY p.created_at DESC
        LIMIT 10
    ''', (doctor_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'doctor': dict(doctor) if doctor else None,
        'assigned_users': [dict(user) for user in assigned_users],
        'consultations': [dict(cons) for cons in consultations]
    })

@doctor_bp.route('/users', methods=['GET'])
def get_assigned_users():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'error': 'Not authorized'}), 401
    
    doctor_id = session['user_id']
    
    conn = get_db_connection()
    users = conn.execute('''
        SELECT u.id, u.username, u.email
        FROM users u
        JOIN assignments a ON u.id = a.user_id
        WHERE a.doctor_id = ?
    ''', (doctor_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@doctor_bp.route('/user/<int:user_id>/predictions', methods=['GET'])
def get_user_predictions(user_id):
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'error': 'Not authorized'}), 401
    
    doctor_id = session['user_id']
    
    # Verify that this user is assigned to this doctor
    conn = get_db_connection()
    assignment = conn.execute('''
        SELECT * FROM assignments WHERE user_id = ? AND doctor_id = ?
    ''', (user_id, doctor_id)).fetchone()
    
    if not assignment:
        conn.close()
        return jsonify({'error': 'User not assigned to this doctor'}), 403
    
    predictions = conn.execute('''
        SELECT id, patient_data, prediction_result, confidence_score, created_at
        FROM predictions
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(pred) for pred in predictions])

@doctor_bp.route('/consultation/update_status', methods=['POST'])
def update_consultation_status():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'error': 'Not authorized'}), 401
    
    data = request.get_json()
    prediction_id = data.get('prediction_id')
    status = data.get('status')
    
    if not prediction_id or not status:
        return jsonify({'error': 'Prediction ID and status are required'}), 400
    
    # In a real application, you would update the status in the database
    # For now, we'll just return a success message
    return jsonify({
        'success': True,
        'message': f'Consultation status updated to {status}',
        'prediction_id': prediction_id
    })

@doctor_bp.route('/patients/search', methods=['GET'])
def search_patients():
    if 'user_id' not in session or session.get('role') != 'doctor':
        return jsonify({'error': 'Not authorized'}), 401
    
    query = request.args.get('q', '')
    doctor_id = session['user_id']
    
    conn = get_db_connection()
    if query:
        users = conn.execute('''
            SELECT u.id, u.username, u.email
            FROM users u
            JOIN assignments a ON u.id = a.user_id
            WHERE a.doctor_id = ? AND u.username LIKE ?
            ORDER BY u.username
        ''', (doctor_id, f'%{query}%')).fetchall()
    else:
        users = conn.execute('''
            SELECT u.id, u.username, u.email
            FROM users u
            JOIN assignments a ON u.id = a.user_id
            WHERE a.doctor_id = ?
            ORDER BY u.username
        ''', (doctor_id,)).fetchall()
    
    conn.close()
    
    return jsonify([dict(user) for user in users])